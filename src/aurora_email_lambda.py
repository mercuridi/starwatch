"""Lambda handler script to create the html content of the email notification"""

def handler(event=None, context=None):
    html_str = """<!DOCTYPE html>
            <html>
            <head>
            <style>
            body {
            font-family:helvetica neue
            }
            </style>
            </head>
            <body>

            <h2>Aurora Alert!</h2>
            <p>It is likely that an aurora will be visible by eye and camera from anywhere in the UK.</p>
            <p>Check the StarWatch dashboard and start planning your night! </p>

            </body>
            </html>
            """
    return {"html": html_str}
