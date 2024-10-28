"""
`rgba`:
  An RGB/RGBA color: is a tuple of 3 integers, representing the red (`0`-`255`), green (`0`-`255`), and blue (`0`-`255`).
  Also includes an optional 4th param, which is a float, that represents the alpha channel (`0.0`-`1.0`).
`hsla`:
  An HSL/HSB color: is a tuple of 3 integers, representing the hue (`0`-`360`), saturation (`0`-`100`), and lightness (`0`-`100`).
  Also includes an optional 4th param, which is a float, that represents the alpha channel (`0.0`-`1.0`).
`hexa`:
  A HEX color: is a string in the format `#RRGGBB` or `#RRGGBBAA` (where `RR`, `GG`, `BB`, and `AA` are hexadecimal digits).

---------------------------------------------------------------------------------------------------------------------------------------
The `Color` class, which contains all sorts of different color-related methods:
- validate colors:
  - is valid rgba
  - is valid hsla
  - is valid hexa
  - is valid in any format
- check if a color has an alpha channel
- convert between different color formats:
  - color to rgba
  - color to hsla
  - color to hexa
- recognize colors inside strings and convert them to color types:
  - string to rgba
- adjust different color channels:
  - brightness
  - saturation
"""


try: from .Regex import *
except: from Regex import *

import re as _re



################################################## CUSTOM TYPES ##################################################
class rgba:
  """An RGB/RGBA color: is a tuple of 3 integers, representing the red (`0`-`255`), green (`0`-`255`), and blue (`0`-`255`).<br>
  Also includes an optional 4th param, which is a float, that represents the alpha channel (`0.0`-`1.0`).\n
  -------------------------------------------------------------------------------------------------------------------------------
  Includes methods:
  - `to_hsla()` to convert to HSL color
  - `to_hexa()` to convert to HEX color
  - `has_alpha()` to check if the color has an alpha channel
  - `lighten(amount)` to create a lighter version of the color
  - `darken(amount)` to create a darker version of the color
  - `saturate(amount)` to increase color saturation
  - `desaturate(amount)` to decrease color saturation
  - `rotate(degrees)` to rotate the hue by degrees
  - `invert()` to get the inverse color
  - `grayscale()` to convert to grayscale
  - `blend(other, ratio)` to blend with another color
  - `is_dark()` to check if the color is considered dark
  - `is_light()` to check if the color is considered light
  - `is_grayscale()` to check if the color is grayscale
  - `is_opaque()` to check if the color has no transparency
  - `with_alpha(alpha)` to create a new color with different alpha
  - `complementary()` to get the complementary color"""
  def __init__(self, r:int, g:int, b:int, a:float = None):
    if any(isinstance(x, rgba) for x in (r, g, b)): raise ValueError('Color is already a rgba() color')
    if not all(isinstance(x, int) and 0 <= x <= 255 for x in (r, g, b)): raise ValueError('RGB color must consist of 3 integers in [0, 255]')
    if not a is None and not (isinstance(a, (int, float)) and 0 <= a <= 1): raise ValueError('Alpha channel must be a float/int in [0.0, 1.0]')
    self.r, self.g, self.b, self.a = r, g, b, (1.0 if a > 1.0 else float(a)) if a else None
    self.h, self.s, self.l = self._rgb_to_hsl(r, g, b)
  def __len__(self): return 4 if self.a else 3
  def __iter__(self): return iter((self.r, self.g, self.b) + ((self.a,) if self.a else ()))
  def __getitem__(self, index): return ((self.r, self.g, self.b) + ((self.a,) if self.a else ()))[index]
  def __repr__(self): return f'rgba({self.r}, {self.g}, {self.b}{f", {self.a}" if self.a else ""})'
  def __str__(self): return f'({self.r}, {self.g}, {self.b}{f", {self.a}" if self.a else ""})'
  def __eq__(self, other):
    if not isinstance(other, rgba): return False
    return (self.r, self.g, self.b) == (other.r, other.g, other.b) and self.a == other.a
  def list(self) -> list:
    """Returns the color components as a list [r, g, b] or [r, g, b, a] if alpha is present"""
    return [self.r, self.g, self.b] + ([self.a] if self.a else [])
  def tuple(self) -> tuple:
    """Returns the color components as a tuple (r, g, b) or (r, g, b, a) if alpha is present"""
    return tuple(self.list())
  def dict(self) -> dict:
    """Returns the color components as a dictionary with keys 'r', 'g', 'b' and optionally 'a'"""
    return dict(r=self.r, g=self.g, b=self.b, a=self.a) if self.a else dict(r=self.r, g=self.g, b=self.b)
  def values(self) -> tuple:
    """Returns the color components as single values r, g, b, a"""
    return self.r, self.g, self.b, self.a
  def to_hsla(self) -> 'hsla':
    """Converts the color to HSLA format"""
    return hsla(self.h, self.s, self.l, self.a)
  def to_hexa(self) -> 'hexa':
    """Converts the color to hexadecimal format, including alpha if present"""
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def has_alpha(self) -> bool:
    """Returns True if the color has an alpha channel"""
    return self.a != None
  def lighten(self, amount:float) -> 'rgba':
    """Creates a lighter version of the color by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_hsla().lighten(amount).to_rgba().values()
    return rgba(self.r, self.g, self.b, self.a)
  def darken(self, amount:float) -> 'rgba':
    """Creates a darker version of the color by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_hsla().darken(amount).to_rgba().values()
    return rgba(self.r, self.g, self.b, self.a)
  def saturate(self, amount:float) -> 'rgba':
    """Increases the saturation by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_hsla().saturate(amount).to_rgba().values()
    return rgba(self.r, self.g, self.b, self.a)
  def desaturate(self, amount:float) -> 'rgba':
    """Decreases the saturation by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_hsla().desaturate(amount).to_rgba().values()
    return rgba(self.r, self.g, self.b, self.a)
  def rotate(self, degrees:int) -> 'rgba':
    """Rotates the hue by the specified number of degrees"""
    self.r, self.g, self.b, self.a = self.to_hsla().rotate(degrees).to_rgba().values()
    return rgba(self.r, self.g, self.b, self.a)
  def invert(self) -> 'rgba':
    """Returns the inverse color"""
    self.r, self.g, self.b = 255 - self.r, 255 - self.g, 255 - self.b
    return rgba(self.r, self.g, self.b, self.a)
  def grayscale(self) -> 'rgba':
    """Converts the color to grayscale using luminance formula"""
    gray = int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
    self.r = self.g = self.b = gray
    return rgba(self.r, self.g, self.b, self.a)
  def blend(self, other:'rgba', ratio:float = 0.5, additive_alpha:bool = False) -> 'rgba':
    """Blends the current color with another color using the specified ratio (`0.0`-`1.0`):<br>
    If `ratio` is `0.0` it means 100% of the current color and 0% of the `other` color (1:0 mixture)<br>
    If `ratio` is `0.5` it means 50% of both colors (1:1 mixture)<br>
    If `ratio` is `1.0` it means 0% of the current color and 100% of the `other` color (0:1 mixture)"""
    if not (isinstance(ratio, (int, float)) and 0 <= ratio <= 1): raise ValueError("'ratio' must be a float/int in [0.0, 1.0]")
    if not isinstance(other, rgba):
      if Color.is_valid_rgba(other): other = rgba(*other)
      else: raise TypeError("'other' must be a valid RGBA color")
    alpha = (other[3] if other[3] is not None else 1) if len(other) > 3 else 1
    ratio *= 2
    self.r = self._clamp(int((self.r * (2 - ratio)) + (other.r * ratio)), 0, 255)
    self.g = self._clamp(int((self.g * (2 - ratio)) + (other.g * ratio)), 0, 255)
    self.b = self._clamp(int((self.b * (2 - ratio)) + (other.b * ratio)), 0, 255)
    if additive_alpha: self.a = self._clamp((self.a * (2 - ratio)) + (alpha * ratio), 0, 1)
    else: self.a = self._clamp((self.a * (1 - (ratio / 2))) + (alpha * (ratio / 2)), 0, 1)
    return rgba(self.r, self.g, self.b, self.a)
  def is_dark(self) -> bool:
    """Returns `True` if the color is considered dark (luminance < 128)"""
    return (0.299 * self.r + 0.587 * self.g + 0.114 * self.b) < 128
  def is_light(self) -> bool:
    """Returns `True` if the color is considered light (luminance >= 128)"""
    return not self.is_dark()
  def is_grayscale(self) -> bool:
    """Returns `True` if the color is grayscale"""
    return self.r == self.g == self.b
  def is_opaque(self) -> bool:
    """Returns `True` if the color has no transparency"""
    return self.a == 1 or self.a is None
  def with_alpha(self, alpha:float) -> 'rgba':
    """Returns a new color with the specified alpha value"""
    if not (isinstance(alpha, (int, float)) and 0 <= alpha <= 1): raise ValueError("'alpha' must be a float/int in [0.0, 1.0]")
    return rgba(self.r, self.g, self.b, alpha)
  def complementary(self) -> 'rgba':
    """Returns the complementary color (180 degrees on the color wheel)"""
    return self.to_hsla().complementary().to_rgba()
  def _clamp(self, value:int|float, min_val:int|float = 0, max_val:int|float = 255) -> int|float:
    return max(min_val, min(max_val, value))
  def _rgb_to_hsl(self, r:int, g:int, b:int) -> tuple:
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2
    if max_c == min_c: h = s = 0
    else:
      delta = max_c - min_c
      s = delta / (1 - abs(2 * l - 1))
      if max_c == r: h = ((g - b) / delta) % 6
      elif max_c == g: h = ((b - r) / delta) + 2
      else: h = ((r - g) / delta) + 4
      h /= 6
    return int(round(h * 360)), int(round(s * 100)), int(round(l * 100))

class hsla:
  """A HSL/HSLA color: is a tuple of 3 integers, representing hue (`0`-`360`), saturation (`0`-`100`), and lightness (`0`-`100`).<br>
  Also includes an optional 4th param, which is a float, that represents the alpha channel (`0.0`-`1.0`).\n
  ------------------------------------------------------------------------------------------------------------------------------------
  Includes methods:
  - `to_rgba()` to convert to RGB color
  - `to_hexa()` to convert to HEX color
  - `has_alpha()` to check if the color has an alpha channel
  - `lighten(amount)` to create a lighter version of the color
  - `darken(amount)` to create a darker version of the color
  - `saturate(amount)` to increase color saturation
  - `desaturate(amount)` to decrease color saturation
  - `rotate(degrees)` to rotate the hue by degrees
  - `invert()` to get the inverse color
  - `grayscale()` to convert to grayscale
  - `blend(other, ratio)` to blend with another color
  - `is_dark()` to check if the color is considered dark
  - `is_light()` to check if the color is considered light
  - `is_grayscale()` to check if the color is grayscale
  - `is_opaque()` to check if the color has no transparency
  - `with_alpha(alpha)` to create a new color with different alpha
  - `complementary()` to get the complementary color"""
  def __init__(self, h:int, s:int, l:int, a:float = None):
    if any(isinstance(x, hsla) for x in (h, s, l)): raise ValueError('Color is already a hsla() color')
    if not (isinstance(h, int) and (0 <= h <= 360) and all(isinstance(x, int) and (0 <= x <= 100) for x in (s, l))): raise ValueError('HSL color must have H in [0, 360] and S L in [0, 100]')
    if not a is None and (not isinstance(a, (int, float)) or not 0 <= a <= 1): raise ValueError('Alpha channel must be a float/int in [0.0, 1.0]')
    self.h, self.s, self.l, self.a = h, s, l, (1.0 if a > 1.0 else float(a)) if a else None
    self.r, self.g, self.b = self._hsl_to_rgb(h, s, l)
  def __len__(self): return 4 if self.a else 3
  def __iter__(self): return iter((self.h, self.s, self.l) + ((self.a,) if self.a else ()))
  def __getitem__(self, index): return ((self.h, self.s, self.l) + ((self.a,) if self.a else ()))[index]
  def __repr__(self): return f'hsla({self.h}, {self.s}, {self.l}{f", {self.a}" if self.a else ""})'
  def __str__(self): return f'({self.h}, {self.s}, {self.l}{f", {self.a}" if self.a else ""})'
  def __eq__(self, other):
    if not isinstance(other, hsla): return False
    return (self.h, self.s, self.l) == (other.h, other.s, other.l) and self.a == other.a
  def list(self) -> list:
    """Returns the color components as a list [h, s, l] or [h, s, l, a] if alpha is present"""
    return [self.h, self.s, self.l] + ([self.a] if self.a else [])
  def tuple(self) -> tuple:
    """Returns the color components as a tuple (h, s, l) or (h, s, l, a) if alpha is present"""
    return tuple(self.list())
  def dict(self) -> dict:
    """Returns the color components as a dictionary with keys 'h', 's', 'l' and optionally 'a'"""
    return dict(h=self.h, s=self.s, l=self.l, a=self.a) if self.a else dict(h=self.h, s=self.s, l=self.l)
  def values(self) -> tuple:
    """Returns the color components as single values h, s, l, a"""
    return self.h, self.s, self.l, self.a
  def to_rgba(self) -> 'rgba':
    """Converts the color to RGBA format"""
    return rgba(self.r, self.g, self.b, self.a)
  def to_hexa(self) -> 'hexa':
    """Converts the color to hexadecimal format, including alpha if present"""
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def has_alpha(self) -> bool:
    """Returns True if the color has an alpha channel"""
    return self.a != None
  def lighten(self, amount:float) -> 'hsla':
    """Creates a lighter version of the color by the specified amount (`0.0`-`1.0`)"""
    if not (isinstance(amount, (int, float)) and 0 <= amount <= 1): raise ValueError("'amount' must be a float/int in [0.0, 1.0]")
    self.l = int(min(100, self.l + (100 - self.l) * amount))
    return hsla(self.h, self.s, self.l, self.a)
  def darken(self, amount:float) -> 'hsla':
    """Creates a darker version of the color by the specified amount (`0.0`-`1.0`)"""
    if not (isinstance(amount, (int, float)) and 0 <= amount <= 1): raise ValueError("'amount' must be a float/int in [0.0, 1.0]")
    self.l = int(max(0, self.l * (1 - amount)))
    return hsla(self.h, self.s, self.l, self.a)
  def saturate(self, amount:float) -> 'hsla':
    """Increases the saturation by the specified amount (`0.0`-`1.0`)"""
    if not (isinstance(amount, (int, float)) and 0 <= amount <= 1): raise ValueError("'amount' must be a float/int in [0.0, 1.0]")
    self.s = int(min(100, self.s + (100 - self.s) * amount))
    return hsla(self.h, self.s, self.l, self.a)
  def desaturate(self, amount:float) -> 'hsla':
    """Decreases the saturation by the specified amount (`0.0`-`1.0`)"""
    if not (isinstance(amount, (int, float)) and 0 <= amount <= 1): raise ValueError("'amount' must be a float/int in [0.0, 1.0]")
    self.s = int(max(0, self.s * (1 - amount)))
    return hsla(self.h, self.s, self.l, self.a)
  def rotate(self, degrees:int) -> 'hsla':
    """Rotates the hue by the specified number of degrees"""
    self.h = (self.h + degrees) % 360
    return hsla(self.h, self.s, self.l, self.a)
  def invert(self) -> 'hsla':
    """Inverts the color by rotating hue by 180 degrees and inverting lightness"""
    self.h = (self.h + 180) % 360
    self.l = 100 - self.l
    return hsla(self.h, self.s, self.l, self.a)
  def grayscale(self) -> 'hsla':
    """Converts the color to grayscale by removing saturation"""
    self.s = 0
    return hsla(self.h, self.s, self.l, self.a)
  def blend(self, other:'hsla', ratio:float = 0.5, additive_alpha:bool = False) -> 'rgba':
    """Blends the current color with another color using the specified ratio (`0.0`-`1.0`):<br>
    If `ratio` is `0.0` it means 100% of the current color and 0% of the `other` color (1:0 mixture)<br>
    If `ratio` is `0.5` it means 50% of both colors (1:1 mixture)<br>
    If `ratio` is `1.0` it means 0% of the current color and 100% of the `other` color (0:1 mixture)"""
    return self.to_rgba().blend(Color.to_rgba(other), ratio, additive_alpha).to_hsla()
  def is_dark(self) -> bool:
    """Returns `True` if the color is considered dark (`lightness < 50`)"""
    return self.l < 50
  def is_light(self) -> bool:
    """Returns `True` if the color is considered light (`lightness >= 50`)"""
    return not self.is_dark()
  def is_grayscale(self) -> bool:
    """Returns `True` if the color is considered grayscale"""
    return self.s == 0
  def is_opaque(self) -> bool:
    """Returns `True` if the color has no transparency"""
    return self.a == 1 or self.a is None
  def with_alpha(self, alpha:float) -> 'hsla':
    """Returns a new color with the specified alpha value"""
    if not (isinstance(alpha, (int, float)) and 0 <= alpha <= 1): raise ValueError("'alpha' must be a float/int in [0.0, 1.0]")
    return hsla(self.h, self.s, self.l, alpha)
  def complementary(self) -> 'hsla':
    """Returns the complementary color (180 degrees on the color wheel)"""
    return hsla((self.h + 180) % 360, self.s, self.l, self.a)
  def _hsl_to_rgb(self, h:int, s:int, l:int) -> tuple:
    h, s, l = h / 360, s / 100, l / 100
    if s == 0: r = g = b = int(l * 255)
    else:
      def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
      q = l * (1 + s) if l < 0.5 else l + s - l * s
      p = 2 * l - q
      r = int(round(hue_to_rgb(p, q, h + 1/3) * 255))
      g = int(round(hue_to_rgb(p, q, h) * 255))
      b = int(round(hue_to_rgb(p, q, h - 1/3) * 255))
    return r, g, b

class hexa:
  """A HEX color: is a string representing a hexadecimal color code with optional alpha channel.\n
  -------------------------------------------------------------------------------------------------
  Supports formats: #RGB, #RGBA, #RRGGBB, #RRGGBBAA (with or without leading #)<br>
  Includes methods:
  - `to_rgba()` to convert to RGB color
  - `to_hsla()` to convert to HSL color
  - `has_alpha()` to check if the color has an alpha channel
  - `lighten(amount)` to create a lighter version of the color
  - `darken(amount)` to create a darker version of the color
  - `saturate(amount)` to increase color saturation
  - `desaturate(amount)` to decrease color saturation
  - `rotate(degrees)` to rotate the hue by degrees
  - `invert()` to get the inverse color
  - `grayscale()` to convert to grayscale
  - `blend(other, ratio)` to blend with another color
  - `is_dark()` to check if the color is considered dark
  - `is_light()` to check if the color is considered light
  - `is_grayscale()` to check if the color is grayscale
  - `is_opaque()` to check if the color has no transparency
  - `with_alpha(alpha)` to create a new color with different alpha
  - `complementary()` to get the complementary color"""
  def __init__(self, color:str):
    if isinstance(color, hexa): raise ValueError('Color is already a hexa() color')
    if not isinstance(color, str): raise TypeError('Color must be a string')
    if not color.startswith('#'): color = f'#{color}'
    color = color.upper()
    if len(color) == 4: self.r, self.g, self.b, self.a = int(color[1] * 2, 16), int(color[2] * 2, 16), int(color[3] * 2, 16), None                             #RGB
    elif len(color) == 5: self.r, self.g, self.b, self.a = int(color[1] * 2, 16), int(color[2] * 2, 16), int(color[3] * 2, 16), int(color[4] * 2, 16) / 255.0  #RGBA
    elif len(color) == 7: self.r, self.g, self.b, self.a = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), None                                 #RRGGBB
    elif len(color) == 9: self.r, self.g, self.b, self.a = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), int(color[7:9], 16) / 255.0          #RRGGBBAA
    else: raise ValueError('Hex color must be in format #RGB, #RGBA, #RRGGBB, or #RRGGBBAA')
  def __len__(self): return 4 if self.a else 3
  def __iter__(self): return iter((f'{self.r:02X}', f'{self.g:02X}', f'{self.b:02X}') + ((f'{int(self.a * 255):02X}',) if self.a else ()))
  def __getitem__(self, index): return ((f'{self.r:02X}', f'{self.g:02X}', f'{self.b:02X}') + ((f'{int(self.a * 255):02X}',) if self.a else ()))[index]
  def __repr__(self): return f'hexa(#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""})'
  def __str__(self): return f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}'
  def __eq__(self, other):
    if not isinstance(other, hexa): return False
    return (self.r, self.g, self.b) == (other.r, other.g, other.b) and self.a == other.a
  def list(self) -> list:
    """Returns the color components as a list of hex strings [R, G, B] or [R, G, B, A] if alpha is present"""
    return [f'{self.r:02X}', f'{self.g:02X}', f'{self.b:02X}'] + ([f'{int(self.a * 255):02X}'] if self.a else [])
  def tuple(self) -> tuple:
    """Returns the color components as a tuple of hex strings (R, G, B) or (R, G, B, A) if alpha is present"""
    return tuple(self.list())
  def dict(self) -> dict:
    """Returns the color components as a dictionary with hex string values for keys 'r', 'g', 'b' and optionally 'a'"""
    return dict(r=f'{self.r:02X}', g=f'{self.g:02X}', b=f'{self.b:02X}', a=f'{int(self.a * 255):02X}') if self.a else dict(r=f'{self.r:02X}', g=f'{self.g:02X}', b=f'{self.b:02X}')
  def values(self) -> tuple:
    """Returns the color components as single values r, g, b, a"""
    return self.r, self.g, self.b, self.a
  def to_rgba(self, round_alpha:bool = True) -> 'rgba':
    """Converts the color to RGBA format"""
    return rgba(self.r, self.g, self.b, (round(self.a, 2) if round_alpha else self.a) if self.a else None)
  def to_hsla(self, round_alpha:bool = True) -> 'hsla':
    """Converts the color to HSLA format"""
    return self.to_rgba(round_alpha).to_hsla()
  def has_alpha(self) -> bool:
    """Returns True if the color has an alpha channel"""
    return self.a is not None
  def lighten(self, amount:float) -> 'hexa':
    """Creates a lighter version of the color by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).lighten(amount).values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def darken(self, amount:float) -> 'hexa':
    """Creates a darker version of the color by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).darken(amount).values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def saturate(self, amount:float) -> 'hexa':
    """Increases the saturation by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).saturate(amount).values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def desaturate(self, amount:float) -> 'hexa':
    """Decreases the saturation by the specified amount (`0.0`-`1.0`)"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).desaturate(amount).values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def rotate(self, degrees:int) -> 'hexa':
    """Rotates the hue by the specified number of degrees"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).rotate(degrees).values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def invert(self) -> 'hexa':
    """Returns the inverse color by rotating hue by 180 degrees and inverting lightness"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).invert().values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def grayscale(self) -> 'hexa':
    """Converts the color to grayscale by removing saturation"""
    self.r, self.g, self.b, self.a = self.to_rgba(False).grayscale().values()
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{f"{int(self.a * 255):02X}" if self.a else ""}')
  def blend(self, other:'hexa', ratio:float = 0.5, additive_alpha:bool = False) -> 'rgba':
    """Blends the current color with another color using the specified ratio (`0.0`-`1.0`):<br>
    If `ratio` is `0.0` it means 100% of the current color and 0% of the `other` color (1:0 mixture)<br>
    If `ratio` is `0.5` it means 50% of both colors (1:1 mixture)<br>
    If `ratio` is `1.0` it means 0% of the current color and 100% of the `other` color (0:1 mixture)"""
    return self.to_rgba(False).blend(Color.to_rgba(other), ratio, additive_alpha).to_hexa()
  def is_dark(self) -> bool:
    """Returns `True` if the color is considered dark (converted `lightness < 50`)"""
    return self.to_hsla(False).is_dark()
  def is_light(self) -> bool:
    """Returns `True` if the color is considered light (`lightness >= 50`)"""
    return self.to_hsla(False).is_light()
  def is_grayscale(self) -> bool:
    """Returns `True` if the color is grayscale (`saturation == 0`)"""
    return self.to_hsla(False).is_grayscale()
  def is_opaque(self) -> bool:
    """Returns `True` if the color has no transparency (`alpha == 1.0`)"""
    return self.to_hsla(False).is_opaque()
  def with_alpha(self, alpha:float) -> 'hexa':
    """Returns a new color with the specified alpha value"""
    if not (isinstance(alpha, (int, float)) and 0 <= alpha <= 1): raise ValueError("'alpha' must be in [0.0, 1.0]")
    return hexa(f'#{self.r:02X}{self.g:02X}{self.b:02X}{int(alpha * 255):02X}')
  def complementary(self) -> 'hexa':
    """Returns the complementary color (180 degrees on the color wheel)"""
    return self.to_hsla(False).complementary().to_hexa()



################################################## COLOR OPERATIONS ##################################################
class Color:
  @staticmethod
  def is_valid_rgba(color:str|list|tuple|dict, allow_alpha:bool = True) -> bool:
    try:
      if isinstance(color, (list, tuple, rgba)):
        if allow_alpha and Color.has_alpha(color): return 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255 and 0 <= color[3] <= 255
        else: return 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255
      elif isinstance(color, dict):
        if allow_alpha and Color.has_alpha(color): return 0 <= color['r'] <= 255 and 0 <= color['g'] <= 255 and 0 <= color['b'] <= 255 and 0 <= color['a'] <= 255
        else: return 0 <= color['r'] <= 255 and 0 <= color['g'] <= 255 and 0 <= color['b'] <= 255
      elif isinstance(color, str): return bool(_re.fullmatch(Regex.rgb_str(), color))
    except: return False

  @staticmethod
  def is_valid_hsla(color:str|list|tuple|dict, allow_alpha:bool = True) -> bool:
    try:
      if isinstance(color, (list, tuple, hsla)):
        if allow_alpha and Color.has_alpha(color): return 0 <= color[0] <= 360 and 0 <= color[1] <= 100 and 0 <= color[2] <= 100 and 0.0 <= color[3] <= 1.0
        else: return 0 <= color[0] <= 360 and 0 <= color[1] <= 100 and 0 <= color[2] <= 100
      elif isinstance(color, dict):
        if allow_alpha and Color.has_alpha(color): return 0 <= color['h'] <= 360 and 0 <= color['s'] <= 100 and 0 <= color['l'] <= 100 and 0.0 <= color['a'] <= 1.0
        else: return 0 <= color['h'] <= 360 and 0 <= color['s'] <= 100 and 0 <= color['l'] <= 100
      elif isinstance(color, str): return bool(_re.fullmatch(Regex.hsl_str(), color))
    except: return False

  @staticmethod
  def is_valid_hexa(color:str, allow_alpha:bool = True) -> bool:
    try:
      if allow_alpha: pattern = r'(?i)^([0-9A-F]{8}|[0-9A-F]{6}|[0-9A-F]{4}|[0-9A-F]{3})$'
      else: pattern = r'(?i)^([0-9A-F]{6}|[0-9A-F]{3})$'
      return bool(_re.fullmatch(pattern, color.lstrip('#')))
    except: return False

  @staticmethod
  def is_valid(color:str|list|tuple|dict, allow_alpha:bool = True) -> bool:
    return Color.is_valid_hexa(color, allow_alpha) or Color.is_valid_rgba(color, allow_alpha) or Color.is_valid_hsla(color, allow_alpha)

  @staticmethod
  def has_alpha(color:rgba|hsla|hexa) -> bool:
    """Check if the given color has an alpha channel.\n
    --------------------------------------------------------------------------------
    Input a HEX or RGB color as `color`.<br>
    Returns `True` if the color has an alpha channel and `False` otherwise."""
    if isinstance(color, (rgba, hsla, hexa)): return color.has_alpha()
    if isinstance(color, str) and Color.is_valid_hexa(color): return len(color.lstrip('#')) == 4 or len(color.lstrip('#')) == 8
    elif isinstance(color, (list, tuple, dict)) and len(color) == 4: return True
    else: return False

  @staticmethod
  def to_rgba(color:hsla|hexa) -> rgba:
    if isinstance(color, (hsla, hexa)): return color.to_rgba()
    if Color.is_valid_hsla(color): return hsla(color[0], color[1], color[2], color[3]).to_rgba() if Color.has_alpha(color) else hsla(color[0], color[1], color[2]).to_rgba()
    if Color.is_valid_hexa(color): return hexa(color).to_rgba()
    raise ValueError('Invalid color format')

  @staticmethod
  def to_hsla(color:rgba|hexa) -> hsla:
    if isinstance(color, (rgba, hexa)): return color.to_hsla()
    if Color.is_valid_rgba(color): return rgba(color[0], color[1], color[2], color[3]).to_hsla() if Color.has_alpha(color) else rgba(color[0], color[1], color[2]).to_hsla()
    if Color.is_valid_hexa(color): return hexa(color).to_hsla()
    raise ValueError('Invalid color format')

  @staticmethod
  def to_hexa(color:rgba|hsla) -> hexa:
    if isinstance(color, (rgba, hsla)): return color.to_hexa()
    if Color.is_valid_rgba(color): return rgba(color[0], color[1], color[2], color[3]).to_hexa() if Color.has_alpha(color) else rgba(color[0], color[1], color[2]).to_hexa()
    if Color.is_valid_hsla(color): return hsla(color[0], color[1], color[2], color[3]).to_hexa() if Color.has_alpha(color) else hsla(color[0], color[1], color[2]).to_hexa()
    raise ValueError('Invalid color format')

  @staticmethod
  def str_to_rgba(rgb_str:str) -> rgba|None:
    try: _rgba = _re.match(Regex.rgb_str(allow_alpha=True), rgb_str).groups()
    except: return None
    if _rgba[3] in ['', None]: return rgba(int(_rgba[0]), int(_rgba[1]), int(_rgba[2]))
    else: return rgba(int(_rgba[0]), int(_rgba[1]), int(_rgba[2]), (int(_rgba[3]) if _rgba[3].count('.') == 0 else float(_rgba[3])))

  @staticmethod
  def text_color_for_on_bg(title_bg_color:hexa|rgba = '#FFF') -> hexa|rgba:
    was_hex = False
    if Color.is_valid_hexa(title_bg_color): was_hex, title_bg_color = True, Color.to_rgba(title_bg_color)
    brightness = 0.2126 * title_bg_color[0] + 0.7152 * title_bg_color[1] + 0.0722 * title_bg_color[2]
    return (hexa('#FFF') if was_hex else rgba(255, 255, 255)) if brightness < 128 else (hexa('#000') if was_hex else rgba(0, 0, 0))

  @staticmethod
  def adjust_brightness(color:hexa|rgba, brightness_change:float) -> hexa|rgba:
    """In- or decrease the brightness of the input color.\n
    -----------------------------------------------------------------------------------------------------------------
    **color** (hexa | rgb): HEX or RGB color.<br>
    **brightness_change** (float): A float between -1.0 (darken by `100%`) and 1.0 (lighten by `100%`), inclusive.\n
    -----------------------------------------------------------------------------------------------------------------
    **returns** (hexa | rgb): The adjusted color in the format of the input color."""
    if Color.is_valid_hexa(color): _rgba = Color.to_rgba(color)
    elif Color.is_valid_rgba(color): _rgba = color
    else: raise ValueError(f"Invalid color format '{str(color)}' Use HEX (e.g. '#F00' and '#FF0000') or RGB (e.g. (255, 0, 0) and (255, 0, 0, 1.0))")
    r, g, b, a = _rgba.r, _rgba.g, _rgba.b, _rgba.a if hasattr(_rgba, 'a') else None
    r = int(max(min(r + (255 - r) * brightness_change if brightness_change > 0 else r * (1 + brightness_change), 255), 0))
    g = int(max(min(g + (255 - g) * brightness_change if brightness_change > 0 else g * (1 + brightness_change), 255), 0))
    b = int(max(min(b + (255 - b) * brightness_change if brightness_change > 0 else b * (1 + brightness_change), 255), 0))
    if isinstance(color, (str, hexa)): return Color.to_hexa((r, g, b, a))
    else: return rgba(r, g, b, a) if a else rgba(r, g, b)

  @staticmethod
  def adjust_saturation(color:hexa|rgba, saturation_change:float) -> hexa|rgba:
    if Color.is_valid_hexa(color): _rgb = Color.to_rgba(color)
    elif Color.is_valid_rgba(color): _rgb = color
    else: raise ValueError(f'Invalid color format "{str(color)}". Use HEX (e.g. "#F00" and "#FF0000") or RGB (e.g. (255, 0, 0) and (255, 0, 0, 1.0))')
    hsl = Color.to_hsla(_rgb)
    h, s, l, a = hsl[0], hsl[1], hsl[2], hsl[3]
    s = max(0, min(100, s + saturation_change * 100))
    if isinstance(color, (str, hexa)): return Color.to_hexa(Color.to_rgba((h, s, l, a)))
    return Color.to_rgba((h, s, l, a))
