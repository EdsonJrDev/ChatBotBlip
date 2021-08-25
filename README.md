# ChatBotBlip Notification
A project for ChatBot using Blip

Easiest way to send a notification for a whatsapp client using Blip


## Requirements
- This projects uses "request", a HTTP Library. If necessary, on terminal/cmd, type:
    ```
    cd "your_project_folder"
    pip install requests
    ```
- A Blip account: https://portal.blip.ai/;
- At least a Chabot and a Template created on Blip Plataform;


## Basic structure
```
{
    "id": {{YOUR_OWN_ID}}, # Use it for your own control
    "to": {{WA_ID}}, # Take it by using "ChaBot.request_identity" on this project
    "type": "application/json",
    "content": {
        "type": "template",
        "template": {
            "namespace": {{NAMESPACE_PROVIDED_BY_BLIP_PLATAFORM}},
            "name": {{TEMPLATE_NAME_PROVIDED_BY_BLIP_PLATAFORM}},
            "language": {"code": "pt_BR", "policy": "deterministic"}, # Change for a language you used when creating a template on Blip 
            "components": {{Component structures}} # see below
        }
    }
}
```

## Component structures

### Text var
```
{
    "type": "body",
    "parameters": [
        {
            "type": "text",
            "text": {{1}} # var 1 of template to complete your text like "Sr. Edson"
        },
        {
            "type": "text",
            "text": {{2}} # var 2 of template to complete your text like "Innovation Developer"
        }
        ...
    ]
}
```

### Image
```
{
    "type": "header",
    "parameters": [
        {
            "type": "image",
            "image": {
                "link": {{image_link}} # image link like "https://github.com/fluidicon.png"
            }
        }
    ]
}
```

### Video
```
{
    "type": "header",
    "parameters": [
        {
            "type": "video",
            "video": {
                "link": {{video_link}} # video link like "https://youtu.be/noZnOSpcjYY"
            }
        }
    ]
}
```

### Document
```
{
    "type": "header",
    "parameters": [
        {
            "type": "document",
            "document": {
                "filename": {{document_finame_with_extension}}, # document filename like "my_doc.pdf"
                "link": {{document_link}} # document link like "https://training.github.com/downloads/pt_BR/github-git-cheat-sheet.pdf"
            }
        }
    ]
}
```

### Text button - Quick reply
```
{
    "type": "button",
    "sub_type": "quick_reply",
    "index": {{i}}, # "i" is the index of button. Max. 3 buttons is allowed, so "i" can be 0, 1 or 2 
    "parameters": [
        {"type": "payload", "payload": {{text_button}}} # text of button to used as answer like "OK. I get it!"
    ]
}
...
```

## Methods and properties

Gets a identity of a whatsapp client:
```
ChatBot.request_identity()
```
Params:
- phone - just numbers in format [DDI][DDD][Phone Number] (BR), [Country][Region][Phone Number] (US/Canada), ...;
- id (optional) - use for your own control ("-1" means "not informed" as standard);


Gets the atributtes' values of ChatBot object as a string:
```
ChatBot.to_string()
```
Params:
- no parameters required;


Start sending a message(notification):
```
ChatBot.send_message[.message_type_here()]
```
- Prepare for send a new notification message to whatsapp client using this property.


Send a message of type "text only":
```
ChatBot.send_message.simple_text()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;


Send a message of type "text with quick_reply button":
```
ChatBot.send_message.text_with_quick_reply()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;
- replies (optional) - list of answer options. The option(text) choosen will be the user's answer when button is clicked;


Send a message of type "with image":
```
ChatBot.send_message.with_image()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- image_link - web link of image to be inserted in header of message;
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;


Send a message of type "with video":
```
ChatBot.send_message.with_video()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- video_link - web link of video to be inserted in header of message;
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;


Send a message of type "with document":
```
ChatBot.send_message.with_document()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- document_infos - tuple with data of document: ('filename with extension', 'link of file');
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- text_vars (optional) - tuple of answers. Texts to be inserted in place of template vars;


Allows you send a message using the "components structures" in different ways according to your template:
```
ChatBot.send_message.custom_message()
```
- wa_identity - identity of whatsapp client;
- template - a tuple like ('template_name'*, 'template_namespace'**) containing data of template created on Blip;
- id (optional) - use for your own control ("-1" means "not informed" as standard);
- components (optional) - list containing different types of components that compose the massage. If no components are passed,
then the message will be exactly the same as the template;

.
[*] name given to a model when creating it on Take Blip (check: Selected Bot > ... > Conteúdos on Blip);
[**] namespace of created model on Take Blip (check: Selected Bot > ... > Conteúdos > Selected template_name on Blip);
.

.

.
For more details, check:

https://help.blip.ai/hc/pt-br/articles/360057514334-Como-enviar-notifica%C3%A7%C3%B5es-WhatsApp-via-API-do-Blip#h_01F9HNS021AH2N850WZ661MMNT