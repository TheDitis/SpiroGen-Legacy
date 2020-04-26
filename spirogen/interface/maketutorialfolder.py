import json


textlist = [
            ("Welcome To Spirogen!",
             "This tutorial will guide you through the interface. You can "
             "access this tutorial at any time by finding it in the help "
             "section of the menu bar. \nClick next to start the tutorial!"),
            ("The Pattern Tab",
             "This is the Pattern tab. Here you'll find all of the controls "
             "that determine the shape of the drawing."),
            ("Selecting a Pattern Type",
             "There are a few different pattern types available. Use this menu "
             "to select the type."),
            ("Patern Parameters",
             "This area holds the parameters that determine the form of the "
             "drawing. You'll find things like angle of rotation and pen size "
             "here."),
            ("Drawing the Pattern",
             "- Click the run button to see the pattern drawn. \n- The drawing "
             "will be rendered using the values of the parameters on the page. "
             "\n- Once the drawing is complete, you can exit the drawing "
             "window if you wish."),
            ("Loading & Saving",
             "You can load or save patterns here."),
            ("Loading",
             "- To load a pattern, either type in the name, or click 'List "
             "Available' to get a list of existing settings. \n- Click Load "
             "once name is entered/selected. \n- You can load and save entire "
             "sessions, or color schemes and patterns individually. \n- Make "
             "sure to select the type you are trying to save."),
            ("Tabs",
             "You can control the colors of the drawing in the Color Scheme "
             "tab. Lets take a look at the color controls there."),
            ("The Color Scheme Tab",
             "This is the color scheme control tab.\nYour selections here will "
             "determine the color of the drawing."),
            ("Pattern Color Controls",
             "This is the Pattern color area.\nThese controls determine the "
             "colors of the lines drawn."),
            ("Background Color",
             "This is the Background color section. Just a single RGB color."),
            ("Effects Section",
             "This is the Effects section.\n These transformations alter all of"
             " the colors in your pallete in a permanent way.\n\nNote: GoTo % "
             "values in the Ramp Lightness effect under 30% won't work well."),
            ("Total Colors Control",
             "This control determines the total number of 'inbetween' colors "
             "to render. \n\n- If you have half the total colors that you have "
             "layers/number-of-iterations set in the pattern tab, your color "
             "scheme will repeat twice.\n\n- If you have twice as many total "
             "colors as you have reps set in the pattern, you will only make it"
             " half way through your color scheme.\n\n- The more total colors, "
             "the more gradual the fade from one color to the next."),
            ("Main Color Controls",
             "These are the most important color controls.\n\n- Number of "
             "stops defines how many colors you specifically define.\n\n - "
             "These defined colors are spread evenly across the range of the "
             "number of total colors set.\n\n- If you have only two stops, and "
             "set your total colors to 100, the pattern will start with the "
             "first defined color, and fade with 98 transition colors to the "
             "second color defined.\n\n- The shift control allows you to shift "
             "the position of the colors you have defined.\n\n- You have a bank"
             " of 11 colors total, and when you reduce your number of stops, "
             "you only reduce the number of colors you are currently using, and"
             " shifting will shift through the entire color set.\n\n- Load "
             "Default Colors will load a full-spectrum color set.\n\n- Reverse"
             " order reverses the order of the entire color bank, not just "
             "the currently selected color stops, so if you reverse, you may "
             "have to use the shift control to find your previous position."),
            ("Number of Color Stops",
             "This is the number of colors that you want to define explicitly "
             "to be spread out accross the range of total colors"),
            ("Color Shifting",
             "This control shifts your current selection through all 11 of "
             "the colors in the colorbank."),
            ("Updating Values",
             "You can enter RGB values directly. RGB values must be between 0 "
             "and 255."),
            ("Editing Color Swatches Directly",
             "Clicking on any color swatch will open up an editing dialog, "
             "where you can manipulate the individual channels of that color "
             "directly.\n\n- The swatches on the left of the dialog can be "
             "selected.\n\n- The coluumn of swatches on the left are the "
             "colors in your bank\n\n- The swatches in the right column are "
             "defaults, so the right and left column will be exactly the same "
             "if you haven't edited any of your colors yet.\n\n- You can "
             "paste a hex color code into the hex box, and the color will be "
             "updated."),
            ("Have Fun!",
             "That's it for the tutorial! Enjoy the playground!\n\nThis "
             "tutorial will no longer open upon launch, but you can always "
             "find this tutorial in the Help section of the menu bar.")
]

imagelist = [
            "TutorialWelcome.gif", "PatternTabTut1.png", "PatternTabTut2.png",
            "PatternTabTut3.png", "PatternTabTut4.png","PatternTabTut5.png",
            "LoadingTut1.gif", "PatternTabTut6.png", "ColorSchemeTabTut0.png",
            "ColorSchemeTabTut1.png", "ColorSchemeTabTut2.png",
            "ColorSchemeTabTut3.png", "ColorSchemeTabTut4.png",
            "ColorSchemeTabTut5.png", "NStops.gif", "ColorShift.gif",
            "UpdateColors.gif", "ColorEditDialog.gif", "TutorialWelcome.gif"
]


def main():
    pagelist = []
    for i in range(len(textlist)):
        obj = {}

        pageinfo = list(textlist[i])
        obj['title'] = pageinfo[0]
        obj['text'] = pageinfo[1]
        obj['image'] = imagelist[i]
        pagelist.append(obj)
    with open('settings/tutorial/tutorial_pages.json', 'w') as file:
        json.dump(pagelist, file, indent=2)


if __name__ == "__main__":
    main()