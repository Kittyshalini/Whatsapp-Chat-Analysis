import streamlit as st
import whatsappchatanalysis, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt", accept_multiple_files=False)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = whatsappchatanalysis.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list = list(set(df['user']))  # or however you are getting user_list
    user_list = [str(u) for u in user_list]  # Convert all items to strings
    user_list.sort()
    user_list.remove('nan')
    user_list.insert(0,'overall')
    selected = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Number of messages")
            st.title(helper.fetch_stats(selected, df))
        with col2:
            st.header("Total Number of words")
            st.title(helper.fetch_words(selected, df))
        with col3:
            st.header("Total Number of Media files")
            st.title(helper.fetch_media(selected, df))
        with col4:
            st.header("Total Number of Links")
            st.title(helper.fetch_links(selected, df))

        if selected == 'overall':
            st.title("Most Busy user")
            x = helper.fetch_busy(df)
            fig, ax = plt.subplots()
        
            col1 ,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                st.pyplot(fig)

            with col2:
                st.dataframe(x)

        col1, = st.columns(1)

        with col1:
            df_wc = helper.wordcloud_creater(selected, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        list1 = helper.fetch_emoji(selected, df)

        with col1:    
            st.title("Number of emojis")
            st.title(len(list1))

        with col2:
            st.title("Top 5 emojis")
            st.dataframe(list1[0:5])

        col1, col2 = st.columns(2)

        with col1:
            st.header("First message")
            st.text(helper.first_msg(selected, df))