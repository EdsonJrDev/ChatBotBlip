from requests import post
import urllib

class ChatBot:
    """
        Methods and standards for easly use Blip API.
        About this project:
        https://github.com/EdsonJrDev/ChatBotBlip
        How Take Blip ChatBot API works:
        https://help.blip.ai/hc/pt-br/articles/360057514334-Como-enviar-notifica%C3%A7%C3%B5es-WhatsApp-via-API-do-Blip#h_01F9HNS021AH2N850WZ661MMNT
    """

    MESSAGES_URL = "https://http.msging.net/messages"
    COMMANDS_URL = "https://http.msging.net/commands"
    NOTIFICATIONS_URL = "https://http.msging.net/notifications"

    def __init__(self, auth_key):
        self.authorization_key = auth_key
        self.HEADERS = {
            "Authorization": self.authorization_key,
            "Content-Type": "application/json"
        }

    def request_identity(self, phone, id="-1"):
        """
            Gets the identity of a whatsapp client.

            params:
                - phone - just numbers in format [DDI][DDD][Phone Number] (BR), [Country][Region][Phone Number] (US/Canada), ...;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);

            return:
                String with identity of whatsapp client
        """

        data = {
            "id": id,
            "to": "postmaster@wa.gw.msging.net",
            "method": "get", 
            "uri": "lime://wa.gw.msging.net/accounts/+"+phone
        }

        response = post(self.COMMANDS_URL, headers=self.HEADERS, json=data).json()

        return "" if(response["status"] == 'failure') else response['resource']['alternativeAccount']

    @property
    def send_message(self):
        """
            Prepare for send a new notification message to whatsapp client.
        """

        return MessageType(self.MESSAGES_URL, self.authorization_key)

    @property
    def send_email(self):
        """
            Prepare for send a new notification message to whatsapp client.
        """

        return EmailType(self.MESSAGES_URL, self.authorization_key)

    def to_string(self):
        print("""
        MESSAGES_URL = {}
        COMMANDS_URL = {}
        NOTIFICATIONS_URL = {}
        authorization_key = {}
        HEADERS = {{"Authorization": {}, "Content-Type": {}}}
        """.format(
            self.MESSAGES_URL, self.COMMANDS_URL, self.NOTIFICATIONS_URL,
            self.authorization_key, self.HEADERS["Authorization"], self.HEADERS["Content-Type"]
        ))


class MessageType:
    """
        Defines the methods for message types which Bot can work with.
        Pay atention! The message type which must be used depends on template type pre approved by Whatsapp on Take Blip.
    """

    def __init__(self, message_url, authorization_key):
        self.url = message_url
        self.headers = {
            "Authorization": authorization_key,
            "Content-Type": "application/json"
        }

    def custom_message(self, wa_identity, template, id="-1", components=[]):
        """
            Sends a custom message to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - components (optional) - list containing different types of components that compose the massage. If no components are passed,
                then the message will be exactly the same as the template;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

                More infos:
                https://github.com/EdsonJrDev/ChatBotBlip
                https://help.blip.ai/hc/pt-br/articles/360057514334-Como-enviar-notifica%C3%A7%C3%B5es-WhatsApp-via-API-do-Blip#h_01F9HNS8H1E3XVZ91K0NCZ2K2A

            return:
                Object JSON with response of Blip API
        """

        message = {
            "id": id,
            "to": wa_identity,
            "type": "application/json",
            "content": {
                "type": "template",
                "template": {
                    "namespace": template[1],
                    "name": template[0],
                    "language": {"code": "pt_BR", "policy": "deterministic"},
                    "components": components
                }
            }
        }
        response = post(self.url, headers=self.headers, json=message)
        
        return response

    def simple_text(self, wa_identity, template, id="-1", text_vars=()):
        """
            Sends a simple text message to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

            return:
                Object JSON with reponse of Blip API
        """

        components = []
        if(text_vars):
            params = list(map(lambda txt: {"type": "text", "text": txt}, text_vars))
            components = [{
                "type": "body",
                "parameters": params
            }]
        
        return self.custom_message(wa_identity, template, id, components)

    def text_with_quick_reply(self, wa_identity, template, id="-1", text_vars=(), replies=[]):
        """
            Sends a text message with pre-formated answers(buttons) to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;
                - replies (optional) - list of answer options. The option(text) choosen will be the user's answer when button is clicked;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

            return:
                Object JSON with reponse of Blip API
        """

        components = []
        if(text_vars):
            params = list(map(lambda txt: {"type": "text", "text": txt}, text_vars))
            components = [{
                "type": "body",
                "parameters": params
            }]
        i = 0
        for reply in replies:
            components.append({
                "type": "button",
                "sub_type": "quick_reply",
                "index": i,
                "parameters": [
                    {"type": "payload", "payload": reply}
                ]
            })
            i = i + 1

        return self.custom_message(wa_identity, template, id, components)

    def with_image(self, wa_identity, template, image_link, id="-1", text_vars=()):
        """
            Sends a image with optional text message to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - image_link - web link of image to be inserted in header of message;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

            return:
                Object JSON with reponse of Blip API
        """

        components = [{
            "type": "header",
            "parameters": [
                {
                    "type": "image",
                    "image": {
                        "link": image_link
                    }
                }
            ]
        }]
        if(text_vars):
            params = list(map(lambda txt: {"type": "text", "text": txt}, text_vars))
            components.append({
                "type": "body",
                "parameters": params
            })
        
        return self.custom_message(wa_identity, template, id, components)

    def with_video(self, wa_identity, template, video_link, id="-1", text_vars=()):
        """
            Sends a video with optional text message to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - video_link - web link of video to be inserted in header of message;
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

            return:
                Object JSON with reponse of Blip API
        """

        components = [{
            "type": "header",
            "parameters": [
                {
                    "type": "video",
                    "video": {
                        "link": video_link
                    }
                }
            ]
        }]
        if(text_vars):
            params = list(map(lambda txt: {"type": "text", "text": txt}, text_vars))
            components.append({
                "type": "body",
                "parameters": params
            })
        
        return self.custom_message(wa_identity, template, id, components)

    def with_document(self, wa_identity, template, document, id="-1", text_vars=()):
        """
            Sends a document with optional text message to whatapp client "wa_identity".

            params:
                - wa_identity - identity of whatsapp client;
                - template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
                - document_infos - tuple with data of document: ('filename with extension', 'link of file');
                - id (optional) - use for your own control ("-1" means "not informed" as standard);
                - text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;

                [*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
                [**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);

            return:
                Object JSON with reponse of Blip API
        """

        components = [{
            "type":"header",
            "parameters": [
                {
                    "type":"document",
                    "document":{
                        "filename": document[0],
                        "link": document[1]
                    }
                }
            ]
        }]
        if(text_vars):
            params = list(map(lambda txt: {"type": "text", "text": txt}, text_vars))
            components.append({
                "type": "body",
                "parameters": params
            })
        
        return self.custom_message(wa_identity, template, id, components)

class EmailType:
    """
        Defines the methods for email types which Bot can work with.
        Nowadays, only text/plain type for email is possible using Take Blip.

        https://help.blip.ai/hc/pt-br/articles/360057495374-Como-enviar-email-pelo-bot-atrav%C3%A9s-do-Builder
    """

    def __init__(self, message_url, authorization_key):
        self.url = message_url
        self.headers = {
            "Authorization": authorization_key,
            "Content-Type": "application/json"
        }

    def simple_text(self, mail_to, mail_text):
        mail_to = urllib.parse.quote_plus(mail_to)
        message = {
            "to": mail_to+"@mailgun.gw.msging.net",
            "type": "text/plain",
            "content": mail_text
        }

        response = post(self.url, headers=self.headers, json=message)
        
        return response

