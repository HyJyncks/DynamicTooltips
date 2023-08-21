# DynamicTooltips
Adds floating tooltips to your renpy project, allowing singular or a list of images, ints, floats, and full objects to be displayed. This is the Python 3 version and works in Renpy 8 and above.

## How to Use:

1. Merge the game file with the game file of your Ren'Py project.
2. Run your game and test that it works!

Since it's written to accept almost anything as a tooltip, the only info required on your end is either the tooltip, or a list. If you want to display more than one thing at a time. Currently it's only set up to list things vertically, in a vbox, but changing the layout isn't too difficult as I've heavily commented all my code.

I've also made it so it accepts `on show` transforms if you want to get fancy.

```py
screen my_button():
    vbox:
        align (0.5, 0.5)
        textbutton "BUTTON ONE":
            action NullAction()
            tooltip "This is the first tooltip"
        textbutton "BUTTON TWO":
            action NullAction()
            tooltip ["This tooltip also has an image!", "funny_picture.png"]
```

The basic displayable is set up in a screen that is always active in game in overlay screens. If that is not what you want, all you have to do is comment out `config.overlay_screens.append("tooltip_display")` on line 173. Below that, the default usage of the tooltip is defined as `tt` so if you just want to add it to another screen, such as the main menu or navigation, at the bottom of the screen just write `add tt`!

## Creating Your Own Tooltip:

If you wish for a different style of tooltip, I've made it fairly customizable. Allowing text size and style, as well as choosing a different frame, from the one I made and included. You can also set the maximum width for the tooltip as well as any images you may want to use.

The parameters are very self explanitory:
- `text_size` Size of the text in the tooltip

- `text_style` The defined style that you want the text to use.

- `padding` Distance in pixels that the tip or image is offset in x and y

- `spacing` Distance in pixels between items listed in a tooltip with more than one item

- `bg` The path to the background image used by the tooltip
NOTE: image uses a frame object and must be set up to freely scale vertically and horizontally

- `text_xmax` The maximum size in pixels the text can use before a line break

- `img_xmax` The maximum size the image will be horizontally, scaled to fit

For example, the following will make a tooltip with a size of 30, using the style "fancy" provided we have the script font etc:
```py
define MyTooltip = HoverTooltip(text_size = 30, text_style = "fancy")

style fancy:
    font "fonts/my_script_font.otf"
    color "#f00"

screen tooltip_display():
    zorder 100
    add MyTooltip
```

Then you can either add `use tooltip_display` or `add MyTooltip` to the end of your screen of choice, or the aforementioned `config.overlay_screens.append("tooltip_display")` can be, left in if you're using this project, or added to an `init python` block somewhere so it is always visible and ready in game. Again, adding it to `overlay_screens` does not show up in menus, so it would need to be added one of the mentioned ways.

### Terms of Use

If you like it, I'd love to hear about it or see your work. If you want to credit me as `Jnx`, just leave in lines 174 and 175, it adds a little not to `gui.about`. Otherwise just comment it out.
