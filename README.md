
Port of my gamepad/kenney.nl/pygame zero demo to Wasabi2d

To get this demo running on Windows, you first need to install Wasabi2d:
 * Install Python from https://www.python.org/downloads/
 * Install CMake from https://cmake.org/download/
 * In an admin shell, run `python -m pip install virtualenvwrapper-win` (or virtualenvwrapper-powershell)
 * Maybe update pip while you're at it (if it complains)
 * Then in a normal shell, run 
      * `mkvirtualenv wasabi2d` (or `workon wasabi2d` if you're coming back to it later)
      * `python -m pip install wasabi2d` to Install All The Things!
 * Edit wasabi's game.py file to add a handler for joystick axis motion (it should be something like
   C:\Users\<Your Username>\Envs\wasabi2d\Lib\site-packages\wasabi2d\game.py)
   and add this somewhere near line 61 if it isn't already there:
        'on_joyaxis_motion': pygame.JOYAXISMOTION,
 * Finally, you can run this demo:
     `python alien.py`

See <https://www.youtube.com/watch?v=b2IPNCJtUL4> for what the demo looked like before, this one is pretty close

Old Pygame Zero code is available at https://gist.github.com/AnthonyBriggs/f8b4d53cf9387e73fab5badb9cc06417>,
though you'll need my hacked version of pgzero to run it (you can get it from <https://github.com/AnthonyBriggs/pyweek26>)
