# Fluxel Interpreter

Fluxel is a simple, user-friendly scripting language and interpreter designed for creating interactive applications with ease. It provides a range of features for building GUI applications, handling user input, and even integrating with AI models.


## Updates

0.3.0 Added "blast"
blast is a fun little minigame. Press enter to shoot. just make a new line in your code and put "blast" (without the "").

0.2.4 Fixed accidentally deleted interpreter

0.2.3 Added "typewriteask"
Litteraly just typewriter + ask.
example: 
[typewriteask "Hows your day today?" 3
remember userDay
typewrite "You're having a " + userDay + " today? Nice."]

0.2.2	 Added "typewriter"
example: [typewriter "Hello!" 3] Types each letter out and takes 3 seconds to finish.

0.2.0 Added "wait"
example: [wait 3] waits 3 seconds.

## Installation

Install Fluxel using pip:


pip install fluxel
text

## Usage

Run a Fluxel script using the command:


fluxel Script.flux
text

## Features

### Variables and Input

- **Variable Declaration**: `var name = value`
- **User Input**: `ask "Question?"`
- **Remember User Input**: `remember variable_name`

### Output and Interaction

- **Print to Console**: `say "Message" + variable`
- **Pause Execution**: `pause`

### GUI Elements

- **Create Window**: `window "Window Title"`
- **Set Window Size**: `windowsize "width,height"`
- **Add Button**: `button "Button Text" "Command"`
- **Add Label**: `label "Label Text"`
- **Show Window**: `show window`
- **Display Message Box**: `message "Message Text"`

### GUI Input Elements

- **Create Entry Field**: `var entry_name = entry`
- **Create Text Area**: `var text_name = text`
- **Get Entry Value**: `get entry variable_name entry_name`

### AI Integration (Google Gemini) (unfinished)

- **Configure Gemini**: `configure_gemini "API_KEY"`
- **Generate Content**: `generate_content "Prompt"`

### Text Manipulation

- **Append Text**: `append_text variable_name "Text to append"`

### Advanced GUI Features

- **Button with Custom Location**: 

button "Button Text" "Command" objectLocation = x,y
text

## Example Script


window "My First Fluxel App"
windowsize "300,200"
label "Welcome to Fluxel!"
var name_entry = entry
button "Say Hello" "get entry name name_entry
message "Hello, " + name + "!"
"
show window
text

## Notes

- The interpreter automatically adds a pause at the end of each script execution.
- GUI elements are packed vertically by default unless a specific location is provided.
- The Gemini AI integration requires a valid API key from Google.

## Contributing

Contributions to Fluxel are welcome! Please feel free to submit a Pull Request. 

## License

This project is licensed under the GNU GENERAL PUBLIC License - see the LICENSE file for details.