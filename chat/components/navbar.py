import reflex as rx
from chat.state import State

def sidebar_chat(chat: str) -> rx.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return  rx.drawer.close(rx.hstack(
        rx.button(
            chat, on_click=lambda: State.set_chat(chat), width="80%", variant="surface"
        ),
        rx.button(
            rx.icon(
                tag="trash",
                on_click=State.delete_chat,
                stroke_width=1,
            ),
            width="20%",
            variant="surface",
            color_scheme="red",
        ),
        width="100%",
    ))


def sidebar(trigger) -> rx.Component:
    """The sidebar component."""
    return rx.drawer.root(
        rx.drawer.trigger(trigger),
        rx.drawer.overlay(),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.heading("Chats", color=rx.color("mauve", 11)),
                    rx.divider(),
                    rx.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
                    align_items="stretch",
                    width="100%",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="20em",
                padding="2em",
                background_color=rx.color("mauve", 2),
                outline="none",
            )
        ),
        direction="left",
    )


def modal(trigger) -> rx.Component:
    """A modal to create a new chat."""
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.hstack(
                rx.input(
                    placeholder="Type something...",
                    on_blur=State.set_new_chat_name,
                    width=["15em", "20em", "30em", "30em", "30em", "30em"],
                ),
                rx.dialog.close(
                    rx.button(
                        "Create chat",
                        on_click=State.create_chat,
                    ),
                ),
                background_color=rx.color("mauve", 1),
                spacing="2",
                width="100%",
            ),
        ),
    )

def modal_3d_model(trigger) -> rx.Component:
    """A modal to display the 3D model."""
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.vstack(
                rx.html(
                    """
                    <iframe
                    title="Knee Anatomy Model"
                    frameborder="0"
                    allowfullscreen
                    mozallowfullscreen="true"
                    webkitallowfullscreen="true"
                    allow="autoplay; fullscreen; xr-spatial-tracking"
                    xr-spatial-tracking
                    execution-while-out-of-viewport
                    execution-while-not-rendered
                    web-share
                    src="https://sketchfab.com/models/0a2d68c6ec1f4ca783336c96f3c0a5fd/embed"
                    style="width: 500px; height: 500px; max-width: 900px;"
                    >
                    </iframe>
                    """
                ),
                rx.dialog.close(
                    rx.button(
                        "Exit",
                        # on_click=State.create_chat,
                    ),
                ),
                # background_color=rx.color("mauve", 1),
                spacing="8",
                width="100%",
                height="100%",
                align_items="center",
            ),
        ),
    )


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.avatar(src="/kneegpt.png", fallback="UK", variant="solid"),
                rx.heading("U-Knee-Versity"),
                rx.desktop_only(
                    rx.badge(
                    State.current_chat,
                    rx.tooltip(rx.icon("info", size=14), content="The current selected chat."),
                    variant="soft"
                    )
                ),
                align_items="center",
            ),
            rx.hstack(
                modal_3d_model(
                    rx.button(
                        "View 3D Model",
                        rx.icon(
                            tag="rotate-3d",
                            color=rx.color("mauve", 12),
                        ),
                    ), 
                ),
                modal(rx.button(
                    "+ New chat",
                    background_color=rx.color("mauve", 6),
                    )),
                sidebar(
                    rx.button(
                        rx.icon(
                            tag="messages-square",
                            color=rx.color("mauve", 12),
                        ),
                        background_color=rx.color("mauve", 6),
                    )
                ),
                align_items="center",
            ),
            justify_content="space-between",
            align_items="center",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        padding="12px",
        border_bottom=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        position="sticky",
        top="0",
        z_index="100",
        align_items="center",
    )
