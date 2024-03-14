import matplotlib.pyplot as plt
import streamlit as st
import helper
import preprocessor
import seaborn as sns

st.set_page_config(
    page_title="Whatsapp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Whatsapp Chat Analyzer")

st.title("Analysis Space")

uploaded_file = st.file_uploader("Choose a .txt file of any chat - (without media)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()


    # remove changing group name bug
    def remove_substring(data_list, substring):
        flist = [item for item in data_list if substring not in item]
        return flist


    substring_to_remove = "changed the group name"
    user_list = remove_substring(user_list, substring_to_remove)
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis of: ", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, media, links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media)
        with col4:
            st.header("Links Shared")
            st.title(links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        day_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(day_timeline['onlydate'], day_timeline['message'], color='#ff00fb')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#f5ee27')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#8d29ff')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # weekly activity map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis: (Top 5)")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_df = emoji_df.rename(columns={'Emojis': 0, 'Number of times used': 1})
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
