init python:


    import pygame

    class HoverTooltip(renpy.Displayable):
        """
        Displays a dynamic floating tooltip at the mouse position
        
        `text_size`
        Size of the text in the tooltip

        `text_style`
        The defined style that you want the text to use.

        `padding`
        Distance in pixels that the tip or image is offset in x and y

        `spacing`
        Distance in pixels between items listed in a tooltip with more than one item

        `bg`
        The path to the background image used by the tooltip
        NOTE: image uses a frame object and must be able to freely scale vertically and horizontally

        `text_xmax`
        The maximum size in pixels the text can use before a line break

        `img_xmax`
        The maximum size the image will be horizontally, scaled to fit

        """
        
        def __init__(self, text_size = 15, text_style = "default", padding = 10, spacing = 5, bg = "gui/rounded_dt_frame.png", text_xmax = 150, img_xmax = 150, **kwargs):

            super().__init__(**kwargs)
            self.titlesize = text_size
            self.padding = padding
            self.spacing = spacing
            self.text_style = text_style
            self.bg = bg
            self.text_xmax = text_xmax
            self.img_xmax = img_xmax
            self.raw_tip = None
            self.cur_tip = None
            self.old_raw = None
            self.old_tip = None
            self.x = 0
            self.y = 0

        def tip_parse(self, tip):
            val = ''
            # This checks the type of the tooltip
            if type(tip) == str:

                # If the tip is a string, it checks if it's and image first
                # Then just displays text if no image exists
                if any(filter(tip.endswith, [".jpg", ".png", ".webp"])) or renpy.has_image(tip, True):

                    return Transform(tip, xsize = self.img_xmax, fit = "scale-down")
                
                else:

                    val = tip
            
            # If the tooltip is a number, it converts it to a string to display
            elif type(tip) == int or type(tip) == float:

                val = str(tip)
            
            # If the type is a class/object it parses the dictionary of the object
            # displaying it as text. This is less common and if you are doing this I
            # expect you would know how you want this formatted, if not like this.
            else:

                val =  "\n".join("{}: {}".format(k.title(),v) for k, v in tip.__dict__.items())
            
            return Text(val, size = self.titlesize, style = self.text_style)


        def render(self, width, height, st, at):

            if self.cur_tip:

                # This unpacks the tooltip into a vbox for automatic arrangement
                t = VBox(*self.cur_tip, pos = (self.padding, self.padding), spacing = self.spacing, xmaximum = self.text_xmax, fit = "scale-down")

                # Create a render object and get the width and height plus the padding
                cr = renpy.render(t, width, height,st,at)
                w, h = [int(x + self.padding * 2) for x in cr.get_size()]

                # The actual size of the object is set here
                # (By an unfortunately named class that is completely different)
                render = renpy.Render(w,h)

                # This block offsets the tooltip
                # And flips it so it stays on screen
                x = self.x + 10
                if x > config.screen_width - w:
                    x = self.x - w
                y = self.y + 10
                if y > config.screen_height - h:
                    y = self.y - h

                # Create the frame object to be used as a background
                # THIS IS WHERE YOU WOULD EDIT CUSTOM FRAME OPTIONS ---------------------------------------------------------- #######
                if self.bg:
                    bg = Frame( self.bg,
                                Borders (10,10,10,10),
                                xsize = w,
                                ysize = h)

                    # Put the background and image or text into the render
                    render.place(bg, x, y)
                render.place(t, x, y)

                return render

            # Returns nothing if there is no tooltip
            return renpy.Render(0,0)


        def event(self, ev,x,y,st):

            # If the user clicks this will clear the tooltip
            # Just in case the button disappears and prevent the tooltip from staying
            if ev.type == pygame.MOUSEBUTTONUP:
                self.cur_tip = None
                self.raw_tip = None
                renpy.redraw(self,0)

            # Store the x/y coords in the object
            self.x = x
            self.y = y

            if ev.type != pygame.MOUSEMOTION:
                self.raw_tip = GetTooltip()

            if self.raw_tip:
                if self.transform_event != "show":
                    self.set_transform_event("show")

                if self.raw_tip != self.old_raw:

                    if type(self.raw_tip) == list:
                        self.cur_tip = [self.tip_parse(item) for item in self.raw_tip]

                    else:
                        self.cur_tip = [self.tip_parse(self.raw_tip)]
                    
                    self.old_tip = self.cur_tip
                    self.old_raw = self.raw_tip

                else:

                    if self.cur_tip != self.old_tip:
                        self.cur_tip = self.old_tip

            # If there is no tooltip, empty the text to hide it
            # Pending: allowing the hide transform to complete before disappearing
            else:
                if self.transform_event != "hide":
                    self.set_transform_event("hide")

                if self.cur_tip:
                    self.cur_tip = None
                    self.raw_tip = None
            
            renpy.redraw(self,0)

    # This line can be omitted if you want per screen tooltip and
    # is only included for ease of use for less tech-savvy users
    config.overlay_screens.append("tooltip_display")
    if hasattr(gui, "about"):
        gui.about += "\n\nUses {b}{a=https://github.com/HyJyncks/DynamicTooltips}Dynamic Tooltips{/a}{/b} by {color=#7414a0}Jnx{/}"

# Instance the desired tooltip as a variable to add to a screen
# Note that you can style multiple different instances of the tooltip to have different styles per screen!!
define tt = HoverTooltip()
define large_tt = HoverTooltip(30)

transform tt_dis:
    alpha 0.0
    on show:
        ease .5 alpha 1.0
    on hide:
        linear .3 alpha 0

screen tooltip_display():
    zorder 100
    add tt at tt_dis

