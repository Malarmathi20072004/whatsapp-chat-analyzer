import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


sidebar_image = "logo.jpg"  # Replace with the path to your sidebar image

# Use st.sidebar to add the image to the sidebar
st.sidebar.image(sidebar_image)
st.sidebar.title("Whatsapp Chat Analyzer")
import base64
import plotly.express as px
df = px.data.iris()

# Define a function to convert an image file to base64
@st.cache(allow_output_mutation=True)
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the background image URL
background_image_url = "https://webstaging-strapi.knowlarity.com/uploads/What_are_some_m_a8061ce405.png"

# Define the CSS for the background image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url({background_image_url});
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
}}
[data-testid="stToolbar"] {{
    right: 2rem;
}}
</style>
"""

# Apply the background image using st.markdown
st.markdown(page_bg_img, unsafe_allow_html=True)


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode("utf-8")
     df = preprocessor.preprocess(data)

     st.dataframe(df)

     #fetch unique users

     user_list = df['user'].unique().tolist()
     user_list.remove('group_notification')
     user_list.sort()
     user_list.insert(0, "Overall")
     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

     if st.sidebar.button("Show Analysis"):

          num_msgs, words, num_media_msgs, num_links = helper.fetch_stats(selected_user, df)
          st.title("Top Statistics")
          col1, col2, col3, col4 = st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(num_msgs)

          with col2:
               st.header("Total Words")
               st.title(words)

          with col3:
               st.header("Media Shared")
               st.title(num_media_msgs)

          with col4:
               st.header("Links Shared")
               st.title(num_links)

          # timeline
          st.title("Monthly Timeline")
          timeline = helper.monthly_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(timeline['time'], timeline['message'], color = 'green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          st.title("Daily Timeline")
          daily_timeline = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # activity map
          st.title("Activity Map")
          col1, col2 = st.columns(2)

          with col1:
               st.header("Most busy day")
               busy_day = helper.week_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_day.index, busy_day.values, color='green')
               st.pyplot(fig)

          with col2:
               st.header("Most busy month")
               busy_month = helper.month_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values, color='orange')
               st.pyplot(fig)

          st.title("Weekly Activity Map")
          user_heatmap = helper.activity_heatmap(selected_user, df)
          fig, ax = plt.subplots()
          ax = sns.heatmap(user_heatmap)
          st.pyplot(fig)

          # finding the busiest user in the group
          if selected_user == 'Overall':
               st.title("Most Busy Users")
               x, new_df = helper.fetch_most_busy_users(df)
               fig, ax = plt.subplots()

               col1, col2 = st.columns(2)

               with col1:
                    ax.bar(x.index, x.values, color = 'red')
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig)

               with col2:
                    st.dataframe(new_df)

          # wordcloud
          st.title("Wordcloud")
          df_wc = helper.create_word_cloud(selected_user, df)
          fig, ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          # most common words
          st.title("Most Common Words")
          most_common_df = helper.most_common_words(selected_user, df)
          fig, ax = plt.subplots()
          ax.barh(most_common_df[0], most_common_df[1])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          st.title("Project By")
          st.title("21DSC210")
          st.title("M.Malarmathi")