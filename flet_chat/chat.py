import flet as ft

COLORS = [
    ft.Colors.AMBER,
    ft.Colors.BLUE,
    ft.Colors.BROWN,
    ft.Colors.CYAN,
    ft.Colors.GREEN,
    ft.Colors.INDIGO,
    ft.Colors.LIME,
    ft.Colors.ORANGE,
    ft.Colors.PINK,
    ft.Colors.PURPLE,
    ft.Colors.RED,
    ft.Colors.TEAL,
    ft.Colors.YELLOW,
]

OPACITY = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
]


class Message:
    """
    A message from a user that contains text

    Attributes
    ----------
    user : str
        The user that sends a message.
    text : str
        The message itself.
    message_type : str
        The type of the message - login message, chat message
    """

    def __init__(self, user: str, text: str, message_type: str) -> None:
        self.user = user
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    """
    Creates the styling and arrangement of a chat message

    Attributes
    ----------
    message : Message
        The message object.
    """

    def __init__(self, message: Message) -> None:
        super().__init__()
        # display message on the left side
        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.controls = [
            # create an avatar for a user
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user),
            ),
            # style user name and message
            ft.Column(
                [
                    ft.Text(message.user, weight=ft.FontWeight.BOLD),
                    ft.Text(message.text, no_wrap=False),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user: str) -> str:
        """
        Use the first and last letter of the user name for the initials.

        Parameters
        ----------
        user : str
            The username.

        Returns
        ----------
        str
            The initials of the user or a default.
        """

        if user:
            return user[:1].capitalize() + user[-1]
        else:
            return "#"

    def get_avatar_color(self, user: str) -> ft.Colors:
        """
        Create a user specific color and opacity for an avatar.

        Parameters
        ----------
        user : str
            The username.

        Returns
        ----------
        ft.Colors
            The color used for the avatar.
        """

        opacity = OPACITY[hash(user) % len(OPACITY)]
        main_color = COLORS[hash(user) % len(COLORS)]

        color = ft.Colors.with_opacity(opacity, main_color)
        return color


def chat(page: ft.Page) -> None:
    """
    Create a user specific color and opacity for an avatar.

    Parameters
    ----------
    page : ft.Page
        The page for the chat.
    """

    # add ListView for chat
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # add a title for the browser window
    page.title = "Simple Chat"
    # set theme to light instead of system default
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.PURPLE_100,
    )

    # add text field for user name input
    user_name = ft.TextField(
        label="Enter your name",
        autofocus=True,
    )

    # click event for joining the chat
    def join_click(e: ft.RouteChangeEvent) -> None:
        # make sure that a user name is given
        if not user_name.value:
            user_name.error_text = "Please provide a name!"
            user_name.update()
        else:
            # store the user name in the session to use it later
            page.session.set("user_name", user_name.value)
            # close the AlertDialog
            page.close(usr)
            # reroute to the chat now that we have a user name set
            page.route = "/chat"
            # broadcast that a new client is in the chat
            page.pubsub.send_all(
                Message(
                    user=user_name.value,
                    text=f"{user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    # add dialog asking for a user name
    usr = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
    )

    # 'welcome' button - displayed at the start of the chat
    welcome_button = ft.ElevatedButton(
        "Welcome",
        bgcolor="purple100",
        color="black",
        icon="waving_hand_outlined",
        icon_color="black",
        style=ft.ButtonStyle(padding=10),
        on_click=lambda e: page.open(usr),
    )

    # add message broadcasting
    def on_message(message: Message) -> None:
        # differentiate between a chat message and the initial login message to set a user name
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    # subscribe the user to receive messages by broadcast system (pubsub)
    page.pubsub.subscribe(on_message)

    def send_click(e: ft.RouteChangeEvent) -> None:
        # the user id will be the session id for now
        # broadcast the current message in the text field
        page.pubsub.send_all(
            Message(
                user=str(page.session.get("user_name")),
                text=str(new_message.value),
                message_type="chat_message",
            )
        )
        # reset the value of the message for the next input
        new_message.value = ""
        page.update()

    # view for the main page
    main_view = ft.View(
        "/",
        [
            ft.Row(
                [
                    welcome_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
    )

    # add input field for new text message
    new_message = ft.TextField(
        hint_text="Enter a new message...",
        autofocus=True,
        shift_enter=True,
        max_lines=2,
        filled=True,
        expand=True,
        bgcolor="purple100",
        color="black",
        on_submit=send_click,
    )

    # send button for sending a message
    send_button = ft.ElevatedButton("Send", tooltip="Send a message.", icon=ft.Icons.ROCKET, on_click=send_click)

    # view for the chat page
    chat_view = ft.View(
        "/chat",
        [
            chat,
            ft.Row([new_message, send_button]),
        ],
    )

    # add routing for initial page and chat page
    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()
        # add the main welcome page view
        page.views.append(main_view)
        # add the chat page view
        if page.route == "/chat":
            page.views.append(chat_view)

        page.update()

    # event handler - switch to a new view when the route changed
    # the event that's used is ft.RouteChangeEvent
    page.on_route_change = route_change
    page.go(page.route)


ft.app(chat)
