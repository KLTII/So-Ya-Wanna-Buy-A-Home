import streamlit as st

def clean_text(text):
    text = text.replace("`", "").replace("-\n","").replace("\n\n", "&&***&&").replace("\n", " ").replace("&&***&&", "\n\n").strip()
    return (text)

st.title("Lesson 01.02: Intro to Layouts and Images")
st.sidebar.image("HW4.jpg", width=1000)
st.sidebar.header("Options")
text = st.sidebar.text_area("Paste Text Here")
#st.write(text)
button1 = st.sidebar.button("Clean text")
if button1:
    col1, col2 = st.columns(2)
    col1_expander = col1.expander("Expand Original")
    with col1_expander:
#        col1_expander.header("Original Text")
        col1_expander.write(text)
    col2_expander = col2.expander("Expand Cleaned")
    clean = clean_text(text)
    with col2_expander:
#        col2_expander.header("Original Text")
        col2_expander.write(clean)
#    col2.header("Cleaned Text")
    # col2.write(clean)

form1 = st.sidebar.form(key="Options")
form1.header("Params")
form1.multiselect("Select the entities you want to extract", ["Alice", "Rabbit", "Hole"])

text = st.text_area("Sample Text", "Alice enjoys going down the rabbit hole in Wonderland.")

form1.form_submit_button("Click Me")

counter = 0
st.write(counter)
# if st.button("up"):
#     counter = counter+1
#     st.write(counter)

main_container = st.container()
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.write(st.session_state.counter)
if st.button("up"):
    st.session_state.counter += 1
    main_container.write(st.session_state.counter)
    
if st.button("reset"):
    st.session_state.counter = 0
    