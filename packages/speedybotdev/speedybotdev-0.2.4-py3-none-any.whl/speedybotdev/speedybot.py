import json
import urllib.request
from typing import NamedTuple, Callable, List, Dict, Any, Union, Optional
from dataclasses import dataclass, fields, field
from datetime import datetime
import logging
from .speedycard import SpeedyCard
from .consts import SpeedyBotConstants
import random
import re

def is_speedy_card(input) -> bool:
    return isinstance(input, SpeedyCard)

def is_card(card_candidate) -> bool:
    if is_speedy_card(card_candidate):
        return True
    return all(key in card_candidate for key in ('$schema', 'type', 'version'))

## Bare minimum for SpeedyBot to run through steps in Bot.run()
@dataclass(slots=True)
class TidyEnvelopeResult:
    message_id: str
    person_id: str
    resource: str
    room_id: str
    message_type: str

## Current token info
@dataclass(slots=True)
class SelfInfo:
    id: str
    emails: List[str]
    displayName: str
    nickName: str
    userName: str
    avatar: str
    orgId: str
    created: str
    status: str
    type: str # "person" | "bot" | "appuser";
    phoneNumbers: Optional[List[str]] = None  # Optional if empty

@dataclass(slots=True)
class RoomInfo:
    id: str
    title: str
    type: str  # 'direct'/'group'
    isLocked: bool
    lastActivity: str  # ISO 8601 date string
    creatorId: str
    created: str  # ISO 8601 date string
    ownerId: str
    isPublic: bool
    isReadOnly: bool

## Registered webhooks
@dataclass(slots=True)
class Webhook:
    id: str
    name: str
    targetUrl: str
    resource: str
    event: str
    orgId: str
    createdBy: str
    appId: str
    ownedBy: str
    status: str
    created: str
    secret: Optional[str] = None

@dataclass
class WhoAmI:
    self_info: SelfInfo
    webhooks: List[Webhook]
    # id: str
    # name: str
    # resource: str
    # event: str
    # targetUrl: str
    # created: str
    # secret: Optional[str]


@dataclass(slots=True)
class SpeedyFileData:
    url: str
    name: str
    extension: str
    content_type: str
    bytes: int

@dataclass(slots=True)
class MessageResponse:
    id: str
    roomId: str
    roomType: str
    text: str
    personId: str
    personEmail: str
    markdown: str
    created: str
    html: Optional[str] = None
    attachments: Optional[dict] = None

## Helpers for ctx
@dataclass(slots=True)
class CtxAuthor:
    id: str
    email: str
    domain: str
    org: str
    name: str
    type: str
    profilePic: str

@dataclass(slots=True)
class CtxMessage:
    id: str
    roomId: str
    roomType: str
    #mentionedPeople: List[str] = []  # Not modifying vs mentionedPeople: List[str] = field(default_factory=list)
    mentionedPeople: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None

@dataclass
class SpeedyError:
    error_type: str
    error_message: str
    error_args: tuple



trim_api_response = lambda data, cls: {k: v for k, v in data.items() if k in {f.name for f in fields(cls)}}


class SpeedyFile(SpeedyFileData):
    def __init__(self, speedy_file_data: SpeedyFileData, speedy_bot: 'SpeedyBot'):
        super().__init__(
            url=speedy_file_data.url,
            name=speedy_file_data.name,
            extension=speedy_file_data.extension,
            content_type=speedy_file_data.content_type,
            bytes=speedy_file_data.bytes
        )
        self.speedy_bot = speedy_bot

    def fetch_file(self, raw_response: bool = False) -> Any:
        return self.speedy_bot.get_file(self.url, raw_response)




class BotContext:
    def __init__(self, room_id: str, bot: 'SpeedyBot', author: CtxAuthor, msg: CtxMessage, text: Optional[str] = None, file: Optional[SpeedyFile] = None, card: Optional[dict] = None):
        self.room_id = room_id
        self.bot = bot
        self.author = author
        self.msg = msg
        self.text = text
        self.file = file
        self.card = card
        self.next = True
        self.end = False

        
    def send(self, message: Any) -> None:
        """
        Sends a message to the bound room using the SpeedyBot instance.
        """
        # if user passes in a dict that's NOT a SpeedyCard or raw adaptive card spec
        # stringify for them

        if not isinstance(message, str):  # Check if the input is NOT a string
            if not is_card(message):  # Check if anything strange going on
                try:
                    json.dumps(message)  # Test for serializability
                    message = self.build_snippet(message)  # Build the snippet using the message
                except (TypeError, ValueError):
                    raise ValueError("Message is not a valid bot message-- either a string or a SpeedyCard")

        self.bot.send_to(self.room_id, message)

    def reply(self, message: str) -> None:
        """
        Replies to a message in the bound room using the SpeedyBot instance.
        """
        self.bot.send_to(self.room_id, message)

    def card_builder(self) -> 'SpeedyCard':
        return SpeedyCard()
    
    def build_snippet(self, snippet_content, indent=2):
        """
        Builds and sends a snippet message in the Webex space.

        Args:
            snippet_content (any): The content of the snippet to send
            Can be a string or a JSON-serializable object
        
        Returns:
            str: The formatted snippet message.
        """
        if isinstance(snippet_content, (dict, list)):
            snippet_content = json.dumps(snippet_content, indent=indent, sort_keys=True)

        # bummer formatting that unfortunately works 😿 
        snippet_message = f"""```
{snippet_content}
```"""
        return snippet_message


    def clear_screen(self, repeat_count=50):
        """
        Clears the screen in the Webex space by sending a large number of newlines.

        Args:
            repeat_count (int, optional): The number of newlines to send. 
                                          Defaults to 50. Clamped between 1 and 5000.
        """
      
        repeat_count = min(max(1, repeat_count), 5000) 
        clear_screen_message = "\n" * repeat_count
        self.bot.send_to(self.room_id, clear_screen_message)  #

    def http_get(self, url: str, headers: Optional[Dict] = None) -> Any:
        return self.bot._make_request(url, method='GET', headers=headers)

    def http_post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Any:
        return self.bot._make_request(url, method='POST', data=data, headers=headers)

    def fill_template(self, utterances, template):
        # Pick a random utterance
        if isinstance(utterances, list):
            payload = self.pick_random(utterances) or ""
        else:
            payload = utterances

        # Fill in the placeholders in the selected utterance
        for key, value in template.items():
            placeholder = f"${{{key}}}"  # Use ${key} for placeholder
            payload = payload.replace(placeholder, str(value))  # Replace placeholder with value
        
        return payload

    def pick_random(self, items: Union[List[Any], int], max_value: Optional[int] = None) -> Optional[Any]:
        """
        Picks a random item from the provided list of items or integer "between" 2 supplied integers
        """
        if isinstance(items, list):
            return random.choice(items) if items else None
        
        if isinstance(items, int) and max_value is not None:
            return random.randint(items, max_value)


class SpeedyBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.logger = logging.getLogger(self.__class__.__name__)  # Module-specific logger
        self.API = {
            "messages": "https://webexapis.com/v1/messages",
            "attachments": "https://webexapis.com/v1/attachment/actions",
            "webhooks": "https://webexapis.com/v1/webhooks",
            "user": {
                "self": "https://webexapis.com/v1/people/me",
                "person_details": "https://webexapis.com/v1/people"
            },
            "rooms": "https://webexapis.com/v1/rooms"
        }

        self.top_middleware: Optional[Callable] = None
        self.steps: List[Callable[..., Any]] = []
        self.fallback_text = "Your client does not support adaptive cards"
        self.store = {}
        self.error_handler = None


    def on_error(self):
        """
        Sets the error handler for the SpeedyBot instance.
        
        The error handler should take the following parameters:
        - error: an instance of SpeedyError
        - room_id: the ID of the room where the error occurred
        - bot: the SpeedyBot instance itself

        Example usage:
        ```python
        from speedybot import SpeedyBot, SpeedyError
        Bot = SpeedyBot()

        @Bot.on_error()
        def error_handler(error: SpeedyError, room_id: str, bot: SpeedyBot):
            print(f"Error Type: {error.error_type}")
            print(f"Error Message: {error.error_message}")
            print(f"Error Args: {error.error_args}")
    
            # Send a message to the room
             bot.send_to(room_id, f"Sorry, there was an error: {error.error_type} - {error.error_message}")

        ```

        """
        def decorator(fn: Callable):
            self.error_handler = fn
            return fn

        return decorator
    
    def set_log(self, level=logging.DEBUG, log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        logging.basicConfig(level=level, format=log_format)

    def set_fallback_text(self, fallback_message: str) -> None:
        self.fallback_text = fallback_message

    def add_secret(self, key: str, value: str) -> None:
        """Add a secret to the store."""
        self.store[key] = value

    def get_secret(self, key: str) -> str:
        """Retrieve a secret from the store."""
        return self.store.get(key, None)

    def delete_secret(self, key: str) -> None:
        """Delete a secret from the store."""
        if key in self.store:
            del self.store[key]

    def update_secret(self, key: str, value: str) -> None:
        """Update an existing secret in the store."""
        if key in self.store:
            self.store[key] = value

    def clear_secrets(self) -> None:
        """Clear all secrets from the store."""
        self.store.clear()

    ## Pluck out core vales from incoming webhook
    @dataclass(slots=True)
    class TidyEnvelopeResult:
        message_id: str
        person_id: str
        resource: str
        room_id: str
        message_type: str

    def add_step(self, step: Optional[Callable] = None):
        """Add a step to the bot's processing queue."""
        if step:
            if not callable(step):
                raise TypeError(f"Expected a callable, but got {type(step).__name__}")
            self.steps.append(step)
            return step

        def decorator(fn: Callable):
            if not callable(fn):
                raise TypeError(f"Expected a callable, but got {type(fn).__name__}")
            self.steps.append(fn)
            return fn
        return decorator

    def on_text(self, text: Union[str, List[str], Callable, re.Pattern], 
                exact: Optional[bool] = False):
        """Decorator to handle text inputs with string, list, regex, or lambda.
    
    This decorator allows you to specify conditions for text matching, which
    will trigger the associated function when the conditions are met.

    Arguments:
        text (Union[str, List[str], Callable[[str], bool], re.Pattern]): 
            The text condition to match against the incoming message. 
            It can be one of the following:
            
            - A single string: 
              If `exact` is `True`, the function will be called only 
              if the incoming message matches this string exactly.
              If `exact` is `False`, the function will be called if 
              this string is found anywhere in the incoming message.

              Example:

              ```py
              @Bot.on_text('hello', exact=True)
              def greet(ctx):
                  print("Hello!")
              ```

            - A list of strings: 
              The function will be called if any of the strings in 
              the list match the incoming message according to the 
              value of `exact`.

              Example:

              ```py
              @Bot.on_text(['hi', 'hey'], exact=False)
              def greet(ctx):
                  print("Greetings!")
              ```

            - A regular expression (re.Pattern): 
              The function will be called if the incoming message 
              matches the provided regex pattern.

              Example:

              ```py
              @Bot.on_text(re.compile(r'\d+'), exact=False)
              def handle_numbers(ctx):
                  print("Got a number!")
              ```

            - A callable (lambda function or regular function): 
              The function will be called if the callable returns 
              `True` for the incoming message.

              Example:
              ```py
              @Bot.on_text(lambda text: 'urgent' in text.lower())
              def handle_urgent(ctx):
                  print("Urgent message received!")
              ```

        exact (Optional[bool], default=False): 
            Indicates whether to match the incoming message exactly 
            (when applicable). If `True`, exact matches will be required 
            for strings or items in the list.

    Returns:
        Callable: The decorator function to register the callback 
        for the specified text condition.
        """        
        def decorator(fn: Callable):
            self.steps.append(lambda ctx: self.check_text(ctx, text, fn, exact))
            return fn

        return decorator

    def on_file(self, condition: Optional[Callable] = None):
        """Decorator to add a step that reacts to specific file conditions."""
        def decorator(fn: Callable):
            if condition is not None: 
                assert_callable_cond = condition
                self.steps.append(lambda ctx: self.check_file(ctx, assert_callable_cond, fn))
            else:
                # If no condition is provided, just add the function as-is
                self.steps.append(lambda ctx: fn(ctx))
            return fn
        return decorator

    
    def on_card(self, condition: Optional[Callable] = None):
        """Decorator to add a step that reacts to specific file conditions."""
        def decorator(fn: Callable):
            if condition is not None: 
                assert_callable_cond = condition
                self.steps.append(lambda ctx: self.check_card(ctx, assert_callable_cond, fn))
            else:
                self.steps.append(fn)
            return fn
        return decorator

    def check_text(self, ctx, text: Union[str, List[str], Callable, re.Pattern], fn: Callable, exact: Optional[bool] = False):
        message = ctx.text
        match = False  # Default to no match

        # Check for different types of text conditions
        if isinstance(text, str):
            match = (message == text) if exact else (text in message)
        elif isinstance(text, list):
            match = any((message == t) if exact else (t in message) for t in text)
        elif isinstance(text, re.Pattern):
            match = re.search(text, message) is not None
        elif callable(text):
            match = text(message)

        if match:
            try:
                return fn(ctx, message)
            except TypeError:
                return fn(ctx) # fallback if def(ctx: BotContext)

        # Onto next if no match
        return ctx.next


    
    def check_file(self, ctx, condition: Callable, fn):
        if ctx.file is not None:
            file_info = ctx.file
            if condition(file_info):
                try:
                    return fn(ctx, file_info)
                except TypeError:
                    return fn(ctx)

        return ctx.next

    def check_card(self, ctx, condition: Callable, fn):
        if ctx.card is not None:
            card_info = ctx.card 
            if condition(card_info):
                try:
                    # Try calling with both ctx and card, will error if user-supplied function takes single parameter
                    return fn(ctx, card_info)
                except TypeError:
                    # Worst case, they don't include
                    return fn(ctx)

        return ctx.next

    def run(self, payload: Union[Dict, TidyEnvelopeResult]) -> bool:
        """
        Executes the main logic of the SpeedyBot using the provided payload to run Bot.run

        Args:
            payload (Union[Dict, TidyEnvelopeResult]):
                - If providing a dictionary, it must contain the following keys, corresponding to 
                the attributes of `TidyEnvelopeResult`:
                    - 'message_id' (str): Unique identifier of the message.
                    - 'person_id' (str): Unique identifier of the person who sent the message.
                    - 'resource' (str): Type of resource related to the message (e.g., 'text', 'file').
                    - 'room_id' (str): Unique identifier for the room where the message was sent.
                    - 'message_type' (str): Type of message (e.g., 'text', 'attachment').
                    
                Example payload dictionary:
                ```python
                payload = {
                    "message_id": "messageid1234",
                    "person_id": "personid5678",
                    "resource": "text",
                    "room_id": "roomid91011",
                    "message_type": "text"
                }
                ```

                - Alternatively, you can pass an instance of `TidyEnvelopeResult`, which should 
                already encapsulate the above information.
                - You can extract the envelope from a webhook using:
    ```py
    from speedybot import SpeedyBot

    Bot = SpeedyBot()

    # incoming webhook...
    # check secret/validate, etc
    payload = Bot.extract_envelope(webhook)

    # Execute the bot logic with the payload
    success = Bot.run(payload)
    ```

        Returns:
            bool: 
                - Returns True if the bot successfully executed its logic using the provided payload.
                - Returns False if there was an error during execution or if the input was invalid.
        """
        if isinstance(payload, self.TidyEnvelopeResult):
            message_id = payload.message_id
            person_id = payload.person_id
            resource = payload.resource
            room_id = payload.room_id
            message_type = payload.message_type
        elif isinstance(payload, dict):
            message_id = payload.get('message_id', '')
            person_id = payload.get('person_id', '')
            resource = payload.get('resource', '')
            room_id = payload.get('room_id', '')
            message_type = payload.get('message_type', '')

        ## Check author, discard messages sent from bot itself in case webhooks too wide
        self_data = self.get_self()
        proceed = self_data.id != person_id
        if not proceed:
            return False


        # Author
        author_data = self._get_author(person_id)
        author_email = author_data.emails[0].lower()
        author_domain = author_email.split("@")[1]
        
        # Room
        room_data = self.get_room(room_id)

        text = None
        card = None
        file = None
        file_data = None # for "peek" in lambda inside @on_file() decorator
        parent_id = None
        mentioned_people = []

        if message_type == "card":
            card_data = self._get_data(message_type, message_id)
            is_chip = SpeedyBotConstants.chip_label in card_data.get('inputs', {})
            if (is_chip):
                # handle chips
                # message_type = 'text'
                text = card_data['inputs'].get(SpeedyBotConstants.chip_label, '')
            else:
                ## deletes + other interceptions
                is_delete = SpeedyBotConstants.chip_label in card_data.get('inputs', {})
                if (is_delete):
                    self.delete_message(message_id)
                    return True
                
                ## handle delete and other interceptions
                card = card_data.get('inputs', {})

        if message_type in ["text", "file"]:
            data = self._get_data(message_type, message_id)
            text = data.get('text')

            if message_type == "file":
                files = data.get('files', [])
                file_url, *_ = files  # Unpack the first entry into file_url, ignoring the rest
                file_data = self.peek_file(file_url) # @on_file() decorator
                file = SpeedyFile(speedy_file_data=file_data, speedy_bot=self)

        if text:
            self.logger.debug(f"Text is {text}")
            # Trim for group room if needed, ex @botname bongo abc 1234
            if room_data.type == 'group':
                text = " ".join(text.split()[1:])


        # Author data for BotContext
        author_ctx = CtxAuthor(
            id=author_data.id,
            email=author_email,
            domain=author_domain,
            org=author_data.orgId,
            type=author_data.type,
            name=author_data.displayName,
            profilePic=author_data.avatar
        )
        
        message_ctx = CtxMessage(
            id=message_id,
            roomId=room_id,
            roomType=room_data.type,
            mentionedPeople=mentioned_people,
            parent_id=parent_id
        )

        bot_context = BotContext(
            author=author_ctx,
            bot=self,
            card=card,
            file=file,
            msg=message_ctx,
            room_id=room_id,
            text=text
        )

        bot_context.card

        try:
            if self.top_middleware:
                result = self.top_middleware(bot_context)
                if result is False or not result:
                    return False  # Bail out if top step fails
            for step in self.steps:
                    ## do decorator shit somehow...
                    result = step(bot_context)
                    if not result:  # Bail out early if any step returns False or empty
                        break

        except Exception as e:
            error_type = e.__class__.__name__
            error_message = str(e)
            error_args = e.args
            self.logger.error(e)
            if self.error_handler:
                self.error_handler(SpeedyError(error_type=error_type, error_message=error_message, error_args=error_args), room_id, self)
    
        return True

    def extract_envelope(self, envelope: Dict) -> TidyEnvelopeResult:
        """
        Extracts and processes key information from a Webex incoming webhook "envelope"
        
        Note: Ensure that the input envelope has been validated and sanitized for security purposes 
        before calling this function.
        
        Args:
            envelope (Dict): The raw event data received from Webex.

        Returns:
            TidyEnvelopeResult: A dictionary with the extracted message details.
        """
        resource = envelope.get('resource', '')
        data = envelope.get('data', {})
        message_id = data.get('id')
        room_id = data.get('roomId')
        person_id = data.get('personId')
        files = data.get('files', [])
        has_files = len(files) > 0
        is_voice_clip = data.get('isVoiceClip', False)  # Assume the flag is in the data

        # Determine message_type based on the resource and file presence
        if resource == 'attachmentActions':
            message_type = 'card'
        elif resource == 'messages':
            if has_files:
                if is_voice_clip:
                    message_type = 'voice_clip'
                else:
                    message_type = 'file'
            else:
                message_type = 'text'
        else:
            message_type = 'unknown'

        return self.TidyEnvelopeResult(
            message_id=message_id,
            person_id=person_id,
            resource=resource,
            room_id=room_id,
            message_type=message_type
        )

    def set_token(self, token: str):
        """Set the token value."""
        self.token = token

    def get_token(self) -> Optional[str]:
        """Get the current token value."""
        return self.token

    def has_token(self) -> bool:
        """Check if a token is set."""
        return self.token is not None

    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None, headers: Optional[Dict] = None, skip_serial: Optional[bool] = False) -> Any:
        default_header = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        if headers:
            default_header = headers

        request = urllib.request.Request(url, headers=default_header, method=method)

        if data:
            request.data = json.dumps(data).encode()

        with urllib.request.urlopen(request) as response:
            # For HEAD requests (ie peek_fil, return only headers, not body
            if method == "HEAD":
                return dict(response.headers)
            else:
                if skip_serial:
                    return response
                else:
                    return json.loads(response.read().decode())

    def delete_message(self, msg_id: str) -> None:
        url = f"{self.API['messages']}/{msg_id}"
        self._make_request(url, method="DELETE")

    def delete_webhook(self, webhook_id: str) -> None:
        url = f"{self.API['webhooks']}/{webhook_id}"
        self._make_request(url, method="DELETE")

    def get_webhooks(self) -> List[Webhook]:
        url = self.API['webhooks']
        response = self._make_request(url)
        return [Webhook(**item) for item in response.get("items", [])]

    def fetch_webhooks(self) -> List[Dict[str, str]]:
        webhooks = self.get_webhooks()
        return [{"id": w.id, "name": w.name, "resource": w.resource, "targetUrl": w.targetUrl} for w in webhooks]

    def setup_basic_webhooks(self, url: str, secret: Optional[str] = None) -> None:
        self.create_firehose(url, secret)
        self.create_attachment_actions_webhook(url, secret)

    def get_recent_rooms(self, limit: int = 100) -> List[Dict[str, str]]:
        url = f"{self.API['rooms']}?max={limit}&sortBy=lastactivity"
        response = self._make_request(url)
        return [{"type": r["type"], "title": r["title"], "id": r["id"]} for r in response.get("items", [])]

    def create_attachment_actions_webhook(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "attachmentActions",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_attachmentActions",
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_firehose(self, url: str, secret: Optional[str] = None) -> Webhook:
        payload = {
            "resource": "messages",
            "event": "created",
            "targetUrl": url,
            "name": f"{datetime.now().isoformat()}_firehose",
            "secret": secret
        }
        return self.create_webhook(payload)

    def create_webhook(self, payload: Dict[str, Any]) -> Webhook:
        url = self.API['webhooks']
        response = self._make_request(url, method="POST", data=payload)
        return Webhook(**response)

    def get_self(self) -> SelfInfo:
        url = self.API['user']['self']
        response = self._make_request(url)
        return SelfInfo(**response)

    def peek_file(self, url: str) -> SpeedyFileData:
        response = self._make_request(url, method="HEAD")
        return SpeedyFileData(url, **self._extract_file_data(response))

    def get_file(self, url: str, raw_response: bool = False) -> Any:  
        TEXT_EXTENSIONS = {
            "txt", "json", "csv", "xml", "html", "md", "py", "js", "ts", "java", "log"
        }                 
        response = self._make_request(url, headers={"Authorization": f"Bearer {self.token}"}, skip_serial=True)

        # response object if they need to do something special
        if raw_response:
            return response
        
        file_info = self._extract_file_data(response=response.headers)
        extension = file_info.get('extension')
        data = response.read()
        
        # Decode data if txt/csv/etc
        if extension in TEXT_EXTENSIONS:
            return data.decode('utf-8')
        
        return data


    def _extract_file_data(self, response) -> Dict[str, Any]:
        content_type = response.get("Content-Type", "")
        content_disposition = response.get("Content-Disposition", "")
        content_length = int(response.get("Content-Length", 0))

        file_name = content_disposition.split(";")[1].split("=")[1].replace('"', '') if content_disposition else ""
        extension = file_name.split(".")[-1] if file_name else ""

        return {
            'content_type': content_type,
            'name': file_name,
            'extension': extension,
            'bytes': content_length
        }

    def _get_data(self, message_type: str, message_id: str) -> Dict:
        endpoint = f"{self.API['messages']}/{message_id}"
        self.logger.debug(f"[_get_data]: {message_type}, {message_id}: {endpoint}")
        if message_type == 'card':
            endpoint = f"{self.API['attachments']}/{message_id}"
        return self._make_request(endpoint)
        
    
    def _delete_message(self, message_id: str) -> Dict:
        endpoint = f"{self.API['messages']}/{message_id}"
        return self._make_request(endpoint, method='DELETE')
    
    def _get_author(self, person_id: str) -> SelfInfo:
        endpoint = f"{self.API['user']['person_details']}/{person_id}"
        response = self._make_request(endpoint)
        return SelfInfo(**trim_api_response(response, SelfInfo))
    
    def get_room(self, room_id: str) -> RoomInfo:
        endpoint = f"{self.API['rooms']}/{room_id}"
        response = self._make_request(endpoint)
        return RoomInfo(**trim_api_response(response, RoomInfo))

    def send_to(
        self,
        destination: Union[str, Dict[str, str]],
        message: Union[str, 'SpeedyCard', Dict[str, Any]]
    ) -> 'MessageResponse':
        """
    Sends a message to the specified destination with flexible input types.

    Args:
        destination (Union[str, Dict[str, str]]):
            - Destination can be one of the following:
                - 'roomId' (str): The unique identifier of a Webex room.
                - Email address (str): A direct message target by email.
                - Dictionary with 'personId' (e.g., {'personId': 'personId1234'}): Send to a specific Webex user.

        message (Union[str, SpeedyCard, Dict[str, Any]]):
            - The content of the message to send, supporting various formats:
                - A plain string or markdown text.
                - A `SpeedyCard` object, which is an easy-to-use builder for adaptive cards.
                - Raw `SpeedyCard` JSON, which is directly passed as an attachment.
                - A raw JSON dictionary, which will be escaped, formatted, and pretty-printed if not recognized as a card.

    Example:
        ```python
        card = Bot.card().add_title('speedycard title!').add_subtitle('sub title')
        Bot.send_to("joe@joe.com", card)
        ```

    Returns:
        MessageResponse: The Webex API's response object, encapsulating the result of the message send operation.

    This method is the primary function for sending messages in SpeedyBot, handling both simple text messages
    and more complex adaptive card interactions, ensuring fallback content is provided for text-only clients.
    """
        target = self.resolve_destination(destination)
        payload = {**target, "markdown": self.fallback_text, "text": self.fallback_text, "attachments": []}

        if isinstance(message, str):
            payload.update({"markdown": message, "text": message})
        elif isinstance(message, SpeedyCard):
            payload["attachments"].append({
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": message.build()
            })
        elif isinstance(message, dict):
            payload["attachments"].append({
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": message
            })
        else:
            raise ValueError("Invalid message type passed to Bot.send_to")

        response = self._make_request(self.API['messages'], method="POST", data=payload)
        return MessageResponse(**response)

    def _send_to(self, destination: Union[str, Dict[str, str]], message: Union[str, SpeedyFile]) -> MessageResponse:
        target = self.resolve_destination(destination)

        payload = {**target, "markdown": message, "text": message}
        response = self._make_request(self.API['messages'], method="POST", data=payload)
        return MessageResponse(**response)

    def resolve_destination(self, destination: Union[str, Dict[str, str]]) -> Dict[str, str]:
        if isinstance(destination, str):
            if "@" in destination:
                return {"toPersonEmail": destination}
            else:
                return {"roomId": destination}
        return destination
