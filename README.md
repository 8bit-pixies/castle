# castle
You know like...a sand castle in a sandbox or something? Basically a setup to play gym environments

**Why?**

I like creating gym environments. But I want to play inside them too. It would be pretty cool
to create simple games in pure python with like a couple hundred lines of code; even if it is
an ASCII-esque game.

Rendering games as "rgb_array" is nice if you have all the information to do it, but most of the time I don't have it,
nor do I "care" enough.

**How will the game work?**

My intent is that environments will use several conventions(?) (or is it grammatically better to say "semantics") which a generic wrapper will use. These are:

*  `get_board()` - returns a numpy array of 2 or 3 dimensions. If 2 dimensions then it displays the "height x width", if 3 dimensions then it displays "layers x height x width", especially if items can occupied the same position. 
*  `get_info()` - provides the mapping from the numpy array to the icon which is displayed or the sprite which is used

Types of games to target:

-  Games which run based on a "frame-rate" (e.g. atari-esque)
-  Games which wait for input (e.g. solving a path finding environment)

**Goals and Milestones**

*  Ascii wrapper
*  Ascii wrapper with `colorama`
*  Pyglet with ascii
*  Pyglet with sprites

Who knows!


