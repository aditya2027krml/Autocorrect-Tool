import streamlit as st
from symspellpy.symspellpy import SymSpell, Verbosity
from PIL import Image

# Initialize SymSpell object outside the function for efficiency
max_dictionary_edit_distance = 2  # maximum edit distance for corrections
prefix_length = 7  # length of word prefixes to consider
sym_spell = SymSpell(max_dictionary_edit_distance, prefix_length)

# Load the dictionary
dictionary_path = "frequency_dictionary_en_82_765.txt"
term_index = 0  # column of the word
count_index = 1  # column of the frequency

# Load dictionary (Ensure the dictionary exists)
if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
    print("Dictionary file not found or failed to load.")

# Autocorrect function to get top 5 suggestions
def autocorrect_with_suggestions(input_text, max_suggestions=5):
    corrected_sentence = []
    suggestions_list = {}

    for word in input_text.split():
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        
        if suggestions:
            top_suggestions = [suggestion.term for suggestion in suggestions[:max_suggestions]]
            suggestions_list[word] = top_suggestions  # Store top suggestions for each word
            corrected_sentence.append(top_suggestions[0])  # Use the top suggestion as default correction
        else:
            corrected_sentence.append(word)  # If no suggestion, keep the original word
            suggestions_list[word] = [word]  # No suggestions, just the word itself

    return ' '.join(corrected_sentence), suggestions_list

# Streamlit app
def main():
    st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            color: #34495E;
            margin-bottom: 20px;
        }
        .image-container {
            text-align: center;
        }
        .text-input-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .text-input {
            background-color: #e6ffed;
            border: 2px solid #28a745;
            border-radius: 5px;
            padding: 10px;
            font-size: 18px;
            width: 100%;
            color: #333;
        }
        .text-input::placeholder {
            color: #28a745; /* Placeholder color */
            opacity: 1; /* Ensure placeholder is visible */
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">AI-Driven Autocorrect Tool</div>', unsafe_allow_html=True)
    
    # Display author info above the image
    st.markdown('<div class="sub-title">Made by Aditya Kumar</div>', unsafe_allow_html=True)

    # Display image with adjusted size
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("pic1.jpg", caption="Autocorrect Tool", width=400)  # Adjust width as needed
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("This tool detects and corrects incorrect words in real-time. Enter a sentence or word below:")

    # Initialize session state if not already set
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'corrected_text' not in st.session_state:
        st.session_state.corrected_text = ""
    if 'suggestions_list' not in st.session_state:
        st.session_state.suggestions_list = {}

    # Text input with custom CSS class
    st.markdown('<div class="text-input-container">', unsafe_allow_html=True)
    user_input = st.text_input("Enter a word or sentence to autocorrect:", value=st.session_state.input_text, key="user_input", help="Type your text here...")
    st.markdown('</div>', unsafe_allow_html=True)

    # Clear button to reset input
    if st.button("Clear"):
        st.session_state.input_text = ""
        st.session_state.corrected_text = ""
        st.session_state.suggestions_list = {}
        st.experimental_rerun()  # Rerun to clear the text input field

    # Update session state with current input
    st.session_state.input_text = user_input

    # Check if input exists and perform autocorrection
    if user_input:
        with st.spinner("Processing..."):
            corrected_text, suggestions_list = autocorrect_with_suggestions(user_input)
        
        st.session_state.corrected_text = corrected_text
        st.session_state.suggestions_list = suggestions_list

    # Display results
    if st.session_state.corrected_text:
        st.write(f"**Corrected Text:** {st.session_state.corrected_text}")
        
        # Display top 5 suggestions for each word
        st.write("**Top Suggestions for each word:**")
        for word, suggestions in st.session_state.suggestions_list.items():
            st.write(f"**Word:** {word}")
            st.write(f"**Suggestions:** {', '.join(suggestions)}")

if __name__ == "__main__":
    main()
