import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)





    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis On",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words,num_media,num_links = helper.fetch_stats(selected_user,df)

        st.title("Statistics")

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Messages")
            st.title(num_messages)

        with col2:
            st.header("Words")
            st.title(words)

        with col3:
            st.header("Media")
            st.title(num_media)

        with col4:
            st.header("Links")
            st.title(num_links)





        if selected_user == 'Overall':
            st.title("Most Active Users")
            busy, df_user = helper.busy_users(df)
            busy_df = pd.DataFrame({'Users': busy.index, 'Count': busy.values})



            col1, col2, col3 = st.columns(3)

            with col1:
                fig = go.Figure(data=[go.Bar(x=busy_df['Users'], y=busy_df['Count'])])

                fig.update_layout(
                    width=600,
                    height=400,
                    margin=dict(l=50, r=50, t=50, b=50),
                )

                st.plotly_chart(fig)


            with col3:
                st.dataframe(df_user)

        col1,col2 = st.columns(2)
        df_wc = helper.get_wordcloud(selected_user,df)

        with col1:
            st.title("Wordcloud")
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.imshow(df_wc)
            ax.axis('off')
            st.pyplot(fig)

        with col2:
            st.title("Most Common Words")
            most_common_words_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()
            ax.barh(most_common_words_df[0], most_common_words_df[1])
            st.pyplot(fig)


        timeline = helper.monthly_timeline(selected_user,df)
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("Activity Map")
        col1 , col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Heatmap")
        activity_table = helper.activity_heatmap(selected_user,df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_table)
        st.pyplot(fig)

