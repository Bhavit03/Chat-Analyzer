import streamlit as st
import preprocessing,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #   MONTHLY  TIMELINE
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # DAILY TIMELINE
        st.title("Daily Timeline")
        daily_time = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_time['daily_date'], daily_time['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ACTIVITY MAP
        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # BUSIEST USERS IN GROUP
        if selected_user=='Overall':
            st.title("Busiest Users")
            x,new_df=helper.most_busy_users(df)

            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

            st.title("WordCloud")
            df_wc=helper.create_wordcloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
#             MOST COMMON WORDS
        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        st.title("MOST COMMON WORDS")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.dataframe(most_common_df)

#         EMOJI ANALYSIS
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)
#             SENTIMENT
        st.title("SENTIMENT ANALYSIS OF MESSAGES SENT BY USER")
        sentiment_df=helper.sentiment(selected_user,df)
        st.dataframe(sentiment_df)




