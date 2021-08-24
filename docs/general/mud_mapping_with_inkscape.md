### Table of Contents
* **[Quick Reference Guide](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#quick-reference-guide)**
* **[Links and Resources](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#links-and-resources)**
* **[Introduction](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#introduction)**
    * [Why Inkscape?](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#why-inkscape)
* **[Setting Up](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#setting-up)**
    * [Document Properties](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#document-properties)
    * [The Background Layer](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#the-background-layer)
* **[Room Templates](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#room-templates)**
    * [Snapping to the Grid](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#snapping-to-the-grid)
    * [Borders](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#borders)
    * [Pathways](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#pathways)
* **[Mapping](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#mapping)**
    * [Rough Draft](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#rough-draft)
    * [Fine Draft](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#fine-draft)

# Quick Reference Guide

> **TIP:** Open this page into a new tab and keep it positioned on the quick reference guide to easily check it while you work, instead of scrolling up and down on the page.

**Drag Canvas** - `MOUSE WHEEL CLICK + DRAG`

> **TIP:** If you accidentally hold `CTRL` while you attempt to drag the canvas with your mouse wheel, you will instead rotate the canvas. To reset the canvas rotation open the `View` drop-down menu and open `Canvas Orientation` and then select `Reset Rotation`.

**Zoom In / Zoom Out** - `CTRL + MOUSE WHEEL SCROLL`

**Undo Action** - `CTRL + Z`

**Redo Action** - `CTRL + SHIFT + Z`

**Select Multiple Objects** - `SHIFT + LEFT CLICK` | `LEFT CLICK + DRAG`

**Copy Selected Objects** - `CTRL + C`

**Paste Copied Objects** - `CTRL + V`

**Duplicate Selected Objects** - `CTRL + D`

**Group Selected Objects** - `CTRL + G`

**Ungroup Selected Objects** - `CTRL + SHIFT + G`

**Toggle Grid Lines** - `SHIFT + 3`

**Toggle Snapping** - `SHIFT + 5`

**Select and Transform Objects Tool** - `S`

**Raise Object** - `PAGEUP`

**Lower Object** - `PAGEDOWN`

# Links and Resources
> **It's important to read the official documentation on the concepts presented here. This tutorial is not guaranteed to cover all aspects.**

> *To be honest, Inkscape's documentation is all over the place. There are at least 3 different locations, some of them with the same information in a different format. I'm not certain that any of it is up-to-date when it's so scattered.*

**[Inkscape's Home Page](https://inkscape.org/)** - Download the software here.

**[Inkscape Beginners' Guide](https://inkscape-manuals.readthedocs.io/en/latest/index.html)** - Covers all of the most basic topics, including how to install Inkscape.

**[Inkscape Tutorials](https://inkscape.org/learn/)** - Includes written step-by-step tutorials as well as videos.

**[Inkscape Wiki](https://wiki.inkscape.org/wiki/index.php?title=Inkscape)**

**[Inkscape Forums](https://inkscape.org/forums/)**

# Introduction
This tutorial is aimed at those new to Inkscape and image creation programs in general. It attempts to explain things in a step-by-step manner, but don't forget to read up on these features in the official Inkscape documentation. This tutorial is only touching the surface of what this software is capable of and is meant to help you get a start on your MUD map. Feel free to explore and experiment beyond the information presented here.

### Why Inkscape?
Inkscape is a great first choice for making MUD maps because of the easy to use tools for organization. Between the grid, snapping, alignment, and distribution tools, there's plenty at your disposal for keeping your project easy and clean. On top of that, your drawings are in vector graphics. This means that elements on the screen are redrawn any time they are changed, so they can remain consistent even if you decide to resize them later. Raster graphics will have issues scaling up and down after the element is created.

After your project is created, you can share the raw SVG file, allowing others to use what you've built to expand. Players can also use the raw SVG file to see the entire world, zooming in and out as they wish. MUD maps are generally significant in size, as the rooms are cheap and easy to create. The infinite canvas feature in Inkscape allows you to expand forever.

> **WARNING:** You can make objects too large and too many objects in a single file, causing your software to stop responding. Be careful of how much you pile into one project and save frequently. This is really important if you don't have high end hardware.

# Setting Up
When you first start Inkscape, your project will look similar to this.

![Fresh Inkscape Document](https://i.imgur.com/88IMLoi.png)

***

### Document Properties
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

The first thing you want to do is change the document properties. You can access this by using the `File` drop-down menu and selecting `Document Properties...`

![Inkscape Document Properties](https://i.imgur.com/ueig4u9.png)

Change the `Display units:` to `px` for pixels. Uncheck `Show page border` to make the canvas size infinite.
> Don't close the properties window yet!

![Inkscape Page Properties](https://i.imgur.com/acdQeyv.png)

Next, select the `Grids` tab of the `Document Properties` window.

Create a new `Rectangular grid`. Make sure the `Grid units:` is set to pixels.

Set the `Spacing X:` and `Spacing Y:` values to `1`. Set `Major grid line every:` value to `10`. This gives you major grid squares of 10x10 pixels, allowing the 20x20 rooms to have a center point.

Make sure to leave the `Snap to visible grid lines only` enabled. This will be extremely useful, as you will see later.

![Inkscape Grid Properties](https://i.imgur.com/DxvBPRY.png)

Close the `Document Properties` window. Your document should now have grid lines that look like this.

![Inkscape Grid Lines](https://i.imgur.com/WAKd7RV.png)

You may have to zoom in for the minor grid lines to show up. If you see no grid lines at all, check that `Page Grid` is enabled in the `View` drop-down menu. You can also toggle the grid lines on and off using `SHIFT + 3`.

> **BUG:** The `View` drop-down menu sometimes has an unexpected behavior where enabling grid lines toggles them off and vice-versa. Using the `SHIFT + 3` shortcut seems to fix the drop-down menu toggle to behave as intended.

Before you continue, turn snapping off. It's not needed for now and may cause unwanted behavior. You will turn it back on later. You can enable and disable snapping at the top right corner of the document, or by pressing `SHIFT + 5`.

![Inkscape Snapping Toggle](https://i.imgur.com/b16u0h4.png)

***

### The Background Layer
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

Inkscape has two different types of layers. One for the overall canvas and another that deals with each object within the canvas layer. It's best to set up the background layer for your document at the beginning.

There are a few ways to manage your canvas layers. 

1. In the `Layer` drop-down menu, select `Add Layer`... A pop-up box will appear and give you the option to name the layer and decide its position.

![Inkscape Layer Drop-Down Menu](https://i.imgur.com/S4HzLuz.png)

![Inkscape Add Layer Pop-Up](https://i.imgur.com/uYZRMbJ.png)

2. Press `SHIFT + CTRL + L` to open up the `Layers` dock window on the right-hand side of your document. From here you can press the `+` sign to add a new layer and the `Add Layer` pop-up will appear. You can click on the name of a layer in the dock window to rename it at any time. There is also a toggle to make the layer visible or to lock/unlock the layer, as well as arrow icons to help you manage the order of layers.

![Inkscape Layers Dock Window](https://i.imgur.com/XwcAhS7.png)

3. There is also a small layer toolbar element at the bottom left side of your document, but I don't feel it's as useful as the dock window. It has limited options and the drop-down menu can be a bit wonky to select from when there's few layers to list.

![Inkscape Layers Toolbar Element](https://i.imgur.com/HaTgOf5.png)

Create a new layer. Name it `Background` and set its position to the bottom of the document. Scroll really far out on the canvas so that the pixels on the guides along the left and top of the canvas show numbers in the thousands.

Select the Square tool on the left side of the document and `LEFT CLICK + DRAG` across the canvas to make a square about 1,000 by 1,000 pixels. Release `LEFT CLICK`.

If the square isn't already dark green, you can change the color by clicking on the dark green square in the color selector at the bottom left of the document. Alternatively, you can press `SHIFT + CTRL + F` to open the `Fill and Stroke` dock window and set the color manually.

> **TIP:** You should open the `Fill and Stroke` dock regardless, as you will use this often.

> **TIP:** If you need to select an object, press `S` to switch to the `Select and transform objects` tool. It is also the top-most arrow icon on the left toolbar.

If you notice that your background square has a border on it, you can change that by clicking on the `Stroke paint` tab in `Fill and Stroke` and setting it to the same green color as your background or by opening the `Stroke style` tab and changing the width to 0.0 pixels.

You can color the background anything you wish. Green can represent grass, but it is also going to be helpful to contrast the black borders of your room tiles, so you can see where the border is.

![Inkscape Large Green Background Square](https://i.imgur.com/uchcgQ8.png)

Now that our background is set, we want to lock it so that we don't accidentally grab and move it or make any other unintended changes to it.

![Inkscape Lock Background Layer](https://i.imgur.com/0rOI3og.png)

# Room Templates
Now that we have our background set, select the `Layer 1` layer and rename it to something like `Room Template`. Scroll back in on the document near the top left corner so that you can see both the background square and the white canvas. We are going to place our room templates out in the open areas.

### Snapping to the Grid
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

Zoom in/out on your document so that you only see the major grid lines that represent 10x10 pixels. These will represent our room squares.

![Inkscape 10x10 Grid Lines](https://i.imgur.com/nD3rZ3k.png)

Select the square tool or press `R` to swap to it. Make a square approximately the size of the major grid lines. It doesn't have to be perfect, because we will be adjusting it with the snapping feature.

Turn snapping on with `SHIFT + 5` or by selecting it in the top-right corner of the document. Now go down the snapping toolbar and turn off everything, except for the blue grid icon that indicates grid snapping behavior.

![Inkscape Snapping Toolbar Grid Only](https://i.imgur.com/7iUt26k.png)

Change your tool to selection with `S` and if your new room square isn't already selected, click on it to select.

> **TIP:** Note that if you click more than once on an object, the arrows surrounding the object change. The arrows pointing out from the object indicate that it's in scaling transform mode, whereas the rounded arrows indicate it is in rotation transform mode. If you make a mistake, use `CTRL + Z` to undo your last action.

Use the arrows on the corners of the room square to resize the square. Notice the small red `X` in the top-right corner of your square. This is the indicator for snapping. As you can see, the square isn't snapping to the grid just yet.

Now we need to set the behavior of the square's snapping. This is accomplished with the 2nd icon from the top in the snapping toolbar. Click it to enable `Snap bounding boxes`.

![Inkscape Snap Bounding Boxes Toggle](https://i.imgur.com/G7ytlVU.png)

Once this is enabled, you will see 4 more options come alive just below. These options allow us to choose how the bounds of the object will snap. For our purposes, we want to select the 2nd option, `Snap bounding box corners`.

![Inkscape Snap Bounding Box Corners Toggle](https://i.imgur.com/JxMkMA2.png)

Now try to move the corner of the box and you will see the corner snapping to the major grid lines. A little tooltip will pop up to let you know what sort of snapping behavior is happening.

![Inkscape Snap Square Corner To Grid](https://i.imgur.com/AnGF714.png)

We can now fix our square and size it to the boundaries of the major grid lines, making it a perfect 20x20 square.

If your box isn't snapping perfectly, fear not. This is likely a behavior of the border to your square. It can be a bit wonky to deal with.

***

### Borders
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

Before continuing, change the color of your room's square to something other than green, if you haven't already. I suggest starting with a nice 50% gray to represent stone.

![Inkscape Room Tile 50% Gray](https://i.imgur.com/GsSYA7I.png)

No matter the current state of your room's borders, we want to set it properly. Make sure you have your room square selected and go to the `Stroke style` tab of the `Fill and Stroke` dock window (`SHIFT + CTRL + F`).

Change the drop-down menu of the stroke width to pixels and set the width value to 1 pixel, pressing `TAB` to enable the change if you typed out the value. Also make sure that you have the `Miter join` set for the corners, it's the sharp 90° corner and it requires that you have a maximum length set to 1.50 to make the corners sharp. Anything lower than that and the corners will be sliced off.

![Inkscape Stroke Width](https://i.imgur.com/vkuoAzU.png)

> **TIP:** You may have noticed that changing the border's size has messed up the boundaries of your room. Simply adjust the corners again so that the room is aligned with the major grid lines.

If you didn't see anything change, your border may be the same color as the square itself. Either way, we want the border to be black. Open the `Stroke paint` tab of the dock and change it to black by pulling the `V:` slider all the way to the left.

> **TIP:** The color selections at the bottom of your document are only for the object's main color and not the border. As far as I'm aware, you can only change the border's color from the value sliders or the eyedropper tool to pick a color from the canvas.

![Inkscape Black Border](https://i.imgur.com/ncS7AsY.png)

***

### Pathways
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

Nearby your room tile, zoom in so that the grid shows the smaller 1x1 grid squares. Create two new squares of 10x1 pixels, one horizontal and the other vertical. Remove the border, but keep the square's color the same as the room tile.

> **TIP:** The pathway is just a representation of an open space to the next room. The color can be changed to indicate other types of thresholds, such as doors or gates. A slight border could even be added to represent something reinforced, such as a portcullis.

![Inkscape Pathway Square No Border](https://i.imgur.com/4gTeAWq.png)

These little squares will serve as the pathways between each room tile, opening up the border between them and indicating to players that they can travel in that direction.

Move the pathway tile over the room tile so that it covers up the border. Use the major grid line to line up the middle of the pathway with the middle of the room.

![Inkscape Pathway Layering](https://i.imgur.com/qlxZxQI.png)

As part of the template, you want to create various configurations for your room tiles. This approach will help you quickly and easily snap together rooms, without micromanaging every element.

Unselect the pathway tile by clicking off into an open area. Now select just the room itself. `CTRL + C` to copy the room and move your mouse off to the side and use `CTRL + V` to paste. You should now have two rooms.

![Inkscape New Room Copy](https://i.imgur.com/1KDZb8l.png)

Now select the pathway tile just by itself. Copy and paste it in the new room so that it forms a new configuration.

![Inkscape Double Room Pathway](https://i.imgur.com/u4mLxBl.png)

> **TIP:** If you end up with a pathway that isn't showing up over a room, your objects have been created out of order. It's a quick thing to fix. Simply use `PAGEUP` and `PAGEDOWN` to move the object up or down in the object stack.

![Inkscape Pathway Under Room](https://i.imgur.com/LnLp6X6.png)

Once you have your pathways positioned on your room tile, you can select the room and pathways one-by-one with `SHIFT + LEFT CLICK` or altogether by left clicking on an empty space outside of the room and dragging over all elements. 

> **TIP:** Dragging to select will only select elements that are fully encapsulated by the selection box. If you want to select anything that your mouse touches, try holding `ALT + LEFT CLICK` and your mouse pointer will paint a red line on the screen, selecting anything that the line touches.

![Inkscape Red Line Selection](https://i.imgur.com/ufOOE36.png)

With the full room and pathways selected, you can turn the objects into a group with `CTRL + G`. This grouping feature prevents elements from being accidentally selected and dragged by themselves, making the room a whole. `CTRL + SHIFT + G` will ungroup these elements into individual objects once again. 

> **TIP:** Grouping also allows you to change *some* attributes of multiple objects at the same time, such as the color. But be careful of this, as some attributes are not compatible across all objects and you may get unexpected results. `CTRL + Z` will undo your last action.

Continue creating and grouping rooms until you have all possible configurations, including corners and pass-thru rooms. Leave one room and one of each pathway square by themselves, in case you need them later. Check this example image to make sure you've got everything covered. 

![Inkscape Room Template Example](https://i.imgur.com/ma79bGg.png)

Some of these configurations are a little bit redundant, but having more options now may save you time later on; allowing you to place one big unit, instead of multiple smaller units. As you continue mapping, you may find more useful configurations to save as a template or get rid of ones you never use.

> **NOTE:** When working with objects that are only a pixel in width, you may notice that the program seems to show some black outlining around the pathways. That's just an artifact of the software attempting to recalculate what you are viewing based on your zoom level. The following image is an export of my template and it ends up perfect. 

> **TIP:** If you view the exported PNG on a black background, the borders will disappear and it will look like the pathways are sticking out from the rest of the room. You may want to make your borders some offset of black to address such circumstances.

![Inkscape Template PNG Export Example](https://i.imgur.com/kVcNY5b.png)

# Mapping
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

At this point in the tutorial, you should have enough information to get you started. Where you go from here is up to you. There are some basic finishing touches that will be covered, but now that you have your template you can start building your town.

You can start placing elements on your map anywhere you want. If you decide things need to be moved around, you can always select them all and move them. Don't forget to frequently group things you consider "finished". You can always ungroup them if you want to change it later!

Move your template to the area of the map you wish to begin your work. I chose to start making a harbor and wanted the east and south side of my town to be against the ocean. I added a new blue background to represent my ocean. You can choose to add a new layer to work in for the actual map placement itself, if you wish.

***

### Rough Draft
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

The first thing you should do, before starting on the actual map, is make a rough draft. This serves as an outline of where you want things placed. This is a critical step in any creative endeavor. When you write, you start with a first draft. Drawing begins with a sketch. Coding generally begins with pseudo-code. And so on.

Make a new square on your canvas where you can place your idea for locations. You can copy and paste the current green background if you wish, but I'd suggest plotting your map on a new layer.

![Inkscape Map Plot Layer](https://i.imgur.com/6HSoSvE.png)

In this new layer, start placing squares inside it to represent major regions or landmarks of your city or zone.

![Inkscape Map Plot Regions](https://i.imgur.com/vUFPqAO.png)

We want to label these areas so that we know what they are for. Select the `Create and edit text objects` tool, or press `T` to swap to it.

![Inkscape Text and Font Tool](https://i.imgur.com/TijFNyb.png)

Before you even attempt to add text to the canvas, I highly suggest that you open the `Text and Font` dock using `SHIFT + CTRL + T`. It's the best way to manage the properties of your text object.

![Inkscape Text and Font Dock](https://i.imgur.com/PMbfiHi.png)

Now, with the text tool active, click on an empty area where you'd like to add text. It doesn't matter if you are exact; you can move the text object at any time. Type out some text that represents a label for your region.

![Inkscape Seaport Text Label](https://i.imgur.com/tNHOLWe.png)

You can now edit the font size, style, and the text itself via the `Text and Font` dock. Make sure to click `Apply` after any changes.

If you want to move your text, you should switch to the select and transform tool using `S`. 

> **TIP:** Be careful when grabbing a text object. Transforming the text by stretching it with the select tool will distort the height and width ratio. You should really only change the size of your text via the font size within the text and font dock. If you accidentally distort your text, you can simply undo your change with `CTRL + Z` or even delete the text object and make a new one. Changing the font size will not undo a transform on the text object.

![Inkscape Distorted Seaport Text Label](https://i.imgur.com/pHsSsjk.png)

When placing labels, you may want the text to be vertical. In order to accomplish this, select the `Select and Transform` tool with `S` and click on the object. You will see the normal outward arrows that allow you to resize the text object. Click on the text object a second time and the arrows will change to indicate rotation.

![Inkscape Rotate Wharves Text Label](https://i.imgur.com/ApB7pua.png)

You can now select a corner arrow in order to rotate the object. This is a free form rotation, but you may want to be precise in your rotation and fix the text at a vertical 90° angle. Hold `CTRL` while dragging the rotation icon in any of the corners of the text object to snap the rotation to predetermined angles. Your text should now snap at 90°.

Grab your text object and move it into place. Be careful not to grab the cross-hair in the middle of the object. This is the rotation point of the object. Keep this in mind for later; it may come in handy. You can also click on the object again to swap back to the resize mode, removing the cross-hair from the object.

![Inkscape 90 Degree Wharves Text Label](https://i.imgur.com/YlLmhuB.png)

Add some borders to your regions, to help distinguish them from each other. You could also just leave space between each district. Remember that this is a rough outline of what you want your map to be and nothing has to be polished or exact.

![Inkscape Final Rough Draft Map](https://i.imgur.com/oBbYBTr.png)

***

### Fine Draft
[Table of Contents](https://github.com/kovitikus/hecate/wiki/MUD-Mapping-With-Inkscape#table-of-contents)

Make a new large square area nearby your rough draft. With all the skills you've acquired, transform a region of your map into something tangible. Decide on some buildings and landmarks and put it together into a new map.

![Inkscape Seaport Fine Draft](https://i.imgur.com/rOfYs2W.png)

Remember that all of these decisions can be changed later, but you now have a blueprint to work from.