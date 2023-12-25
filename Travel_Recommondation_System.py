# !pip install gensim
# !pip install scikit-learn
# !pip install spacy

from sklearn.metrics.pairwise import cosine_similarity
import spacy
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import requests

nlp = spacy.load("en_core_web_sm")

indian_cities = {
    "Aurangabad": {
        "Weather": ["Tropical", "Hot Summers", "Mild Winters", "Monsoon Season"],
        "Budget": [1000, 3000],
        "Review": "Aurangabad is known for its historical and cultural significance, with attractions like the Ajanta and Ellora Caves. The weather is mostly pleasant, making it a good destination for history enthusiasts."
    },
    "Goa": {
        "Weather": ["Tropical", "Hot and Humid", "Monsoon Season"],
        "Budget": [1500, 5000],
        "Review": "Goa is famous for its beaches, nightlife, and water sports. The weather is tropical, making it a popular destination for tourists looking to relax and enjoy the coastal vibes."
    },
    "Leh Ladakh": {
        "Weather": ["Cold Desert", "Extreme Cold Winters", "Short Summer Season"],
        "Budget": [1000, 4000],
        "Review": "Leh Ladakh is a high-altitude desert region known for its stunning landscapes and Buddhist culture. It's a destination for adventure seekers, especially during the short summer season."
    },
    "Srinagar": {
        "Weather": ["Moderate Summers", "Cold Winters", "Beautiful Spring and Autumn"],
        "Budget": [1200, 4000],
        "Review": "Srinagar, in Jammu and Kashmir, is famous for its scenic Dal Lake and houseboats. It's a place of natural beauty and is best visited during the pleasant spring and autumn seasons."
    },
    "Manali": {
        "Weather": ["Cold", "Snowfall in Winter", "Mild Summers"],
        "Budget": [1000, 3500],
        "Review": "Manali, nestled in Himachal Pradesh, is a popular hill station with snow-capped mountains and adventure activities. It's a great place for both summer and winter vacations."
    },
    "Coorg": {
        "Weather": ["Tropical", "Mild Winters", "Monsoon Season"],
        "Budget": [1500, 4000],
        "Review": "Coorg, also known as Kodagu, is a coffee-producing region in Karnataka. It's known for its lush greenery, waterfalls, and pleasant climate, making it a perfect getaway from city life."
    },
    "Wayanad": {
        "Weather": ["Tropical", "Mild Winters", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Wayanad in Kerala offers a pristine natural environment with forests, waterfalls, and wildlife. It's a great destination for eco-tourism and experiencing the beauty of Western Ghats."
    },
    "Khajuraho": {
        "Weather": ["Tropical", "Hot Summers", "Monsoon Season"],
        "Budget": [800, 2500],
        "Review": "Khajuraho is famous for its UNESCO-listed temples with intricate erotic sculptures. The weather can be hot, so it's best to visit during the cooler months."
    },
    "Jammu and Kashmir": {
        "Weather": ["Varied", "Cold Winters", "Pleasant Summers"],
        "Budget": [1000, 4000],
        "Review": "Jammu and Kashmir offer a diverse range of experiences, from the lush green valleys of Jammu to the snow-covered landscapes of Kashmir. The budget varies depending on the region and season."
    },
    "Himachal Pradesh": {
        "Weather": ["Varied", "Snowfall in Winter", "Pleasant Summers"],
        "Budget": [1000, 4000],
        "Review": "Himachal Pradesh is a state known for its hill stations, including Shimla, Manali, and Dharamshala. It's a popular destination for both adventure and leisure travelers."
    },
    "Uttarakhand": {
        "Weather": ["Varied", "Snowfall in Winter", "Pleasant Summers"],
        "Budget": [1000, 3500],
        "Review": "Uttarakhand offers a mix of adventure and spirituality, with destinations like Rishikesh, Haridwar, and the scenic hill stations of Mussoorie and Nainital."
    },
    "Sikkim": {
        "Weather": ["Varied", "Snowfall in Winter", "Pleasant Summers"],
        "Budget": [1000, 3500],
        "Review": "Sikkim is known for its pristine natural beauty, including lush landscapes and Buddhist monasteries. It's a peaceful destination for those seeking tranquility."
    },
    "Munnar": {
        "Weather": ["Tropical", "Cool Summers", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Munnar, in Kerala, is famous for its tea plantations, misty hills, and cool climate. It's an ideal destination for nature lovers and honeymooners."
    },
    "Lahaul Spiti": {
        "Weather": ["Cold Desert", "Harsh Winters", "Short Summer Season"],
        "Budget": [1000, 3000],
        "Review": "Lahaul and Spiti in Himachal Pradesh offer rugged terrain, Buddhist monasteries, and a unique cold desert landscape. It's a destination for adventure enthusiasts."
    },
    "Mussoorie": {
        "Weather": ["Moderate Summers", "Cold Winters", "Pleasant Spring and Autumn"],
        "Budget": [1000, 3500],
        "Review": "Mussoorie, in Uttarakhand, is a charming hill station with panoramic views of the Himalayas. It's a popular escape for those seeking a break from the city."
    },
    "Jaipur" : {
        "Weather": ["Hot Desert", "Warm Winters"],
        "Budget": [1200, 3500],
        "Review": "Jaipur, the Pink City of Rajasthan, is known for its rich history, palaces, and vibrant culture. It's a great place to explore the royal heritage of India."
    },
    "Varanasi" : {
        "Weather": ["Varied", "Hot Summers", "Pleasant Winters"],
        "Budget": [1000, 3000],
        "Review": "Varanasi, situated on the banks of the Ganges River, is a spiritual and cultural hub. It's famous for its ghats, temples, and ancient traditions."
    },
    "Agra" : {
        "Weather": ["Tropical", "Hot Summers", "Cool Winters"],
        "Budget": [1500, 4000],
        "Review": "Agra is home to the iconic Taj Mahal, a symbol of love and a UNESCO World Heritage site. It's a must-visit destination for history and architecture enthusiasts."
    },
    "Kolkata" : {
        "Weather": ["Tropical", "Hot and Humid Summers", "Mild Winters"],
        "Budget": [1200, 3500],
        "Review": "Kolkata, the cultural capital of India, offers a blend of heritage, art, and cuisine. It's known for its festivals, colonial architecture, and literary history."
    },
    "Rajasthan" : {
        "Weather": ["Varied", "Hot Summers", "Pleasant Winters"],
        "Budget": [1000, 4500],
        "Review": "Rajasthan, the Land of Kings, boasts majestic palaces, forts, and a vibrant culture. It's a diverse state with unique experiences in every city."
    },
    "Kochi" : {
    "Weather": ["Tropical", "Moderate Summers", "Monsoon Season"],
    "Budget": [1500, 4000],
    "Review": "Kochi, in Kerala, is known for its colonial history, backwaters, and seafood cuisine. It offers a blend of culture, history, and natural beauty."
    },
    "Amritsar" : {
        "Weather": ["Varied", "Hot Summers", "Cold Winters"],
        "Budget": [1000, 3000],
        "Review": "Amritsar is famous for the Golden Temple, a spiritual and cultural landmark. It's a place of tranquility and religious significance."
    },
    "Mysuru" : {
        "Weather": ["Tropical", "Mild Winters", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Mysuru, in Karnataka, is renowned for its royal heritage, palaces, and the grand Mysore Dasara festival. It's a city of historical charm."
    },
    "Puducherry" : {
        "Weather": ["Tropical", "Moderate Summers", "Monsoon Season"],
        "Budget": [1000, 3000],
        "Review": "Puducherry, also known as Pondicherry, offers a French colonial vibe, serene beaches, and spiritual experiences at Auroville."
    },
    "Darjeeling" : {
        "Weather": ["Temperate", "Cool Summers", "Monsoon Season"],
        "Budget": [1500, 4000],
        "Review": "Darjeeling, in West Bengal, is famous for its tea gardens, scenic vistas of the Himalayas, and the Darjeeling Himalayan Railway."
    },
    "Hyderabad" : {
        "Weather": ["Tropical", "Hot Summers", "Moderate Winters"],
        "Budget": [1200, 3500],
        "Review": "Hyderabad, the City of Pearls, is known for its rich Nizami heritage, biryani, and iconic landmarks like Charminar and Golconda Fort."
    },
    "Rann of Kutch" : {
        "Weather": ["Desert", "Hot Summers", "Cold Winters"],
        "Budget": [1000, 3000],
        "Review": "The Rann of Kutch, in Gujarat, offers a surreal white desert landscape and hosts the vibrant Rann Utsav festival."
    },
    "Puri" : {
        "Weather": ["Tropical", "Hot Summers", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Puri, in Odisha, is famous for the Jagannath Temple and its scenic beach. It's a place of religious significance and coastal beauty."
    },
    "Udaipur" : {
        "Weather": ["Tropical", "Hot Summers", "Mild Winters"],
        "Budget": [1500, 4000],
        "Review": "Udaipur, the City of Lakes, is known for its majestic palaces, romantic boat rides on Lake Pichola, and royal hospitality."
    },
    "Varkala" : {
        "Weather": ["Tropical", "Moderate Summers", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Varkala, in Kerala, offers stunning cliffside views, pristine beaches, and a relaxed atmosphere. It's a serene getaway."
    },
    "Aizawl" : {
        "Weather": ["Temperate", "Mild Summers", "Monsoon Season"],
        "Budget": [1000, 3000],
        "Review": "Aizawl, the capital of Mizoram, is nestled in the hills and offers a glimpse into the unique Mizo culture and natural beauty."
    },
    "Rishikesh" : {
        "Weather": ["Temperate", "Pleasant Summers", "Monsoon Season"],
        "Budget": [1200, 3500],
        "Review": "Rishikesh, on the banks of the Ganges, is a hub for yoga, spirituality, and adventure sports. It's a place for both relaxation and thrill."
    }
}

def check_cities(indian_cities):
  for i in indian_cities:
    weather = indian_cities[i]['Weather']
    temp = []
    for j in weather:
      temp.extend([word.lower() for word in j.split(" ")])
    stop_words = set(stopwords.words('english'))
    temp = [word for word in temp if word.lower() not in stop_words]
    indian_cities[i]['Weather'] = temp
  return indian_cities

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def similarity(review1, review2):
  p_review1 = nlp(preprocess_text(review1))
  p_review2 = nlp(preprocess_text(review2))

  vector1 = p_review1.vector.reshape(1, -1)
  vector2 = p_review2.vector.reshape(1, -1)

  return cosine_similarity(vector1, vector2)[0][0]

def budget_check(val, values):
  return values["Budget"][0] - 1000 <= val <= values["Budget"][1] + 1000 or val >= values["Budget"][1]

class Reccomendation_System:

  def add_feedback(self, review, city):
    if indian_cities[city]['Review']:
      indian_cities[city]['Review'] += f". {review}"
    else:
      indian_cities[city]['Review'] = f". {review}"
    return "Review Added !!"

  def check_preferences(self, user_preferences):
    if user_preferences['Weather'] == []:

      BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
      API_KEY = '5463d254de7033ece194749b8053b1a0'
      city = user_preferences['City']
      url = BASE_URL + "appid=" + API_KEY + "&q=" + city
      response = requests.get(url).json()

      user_preferences['Weather'].append(response['weather'][0]['main'].lower())
      celsius = response['main']['temp'] - 273.15
      if celsius <= 15:
        user_preferences['Weather'].append('cold')
        user_preferences['Weather'].append('winter')
      elif celsius >= 29:
        user_preferences['Weather'].append('hot')
        user_preferences['Weather'].append('warm')

      if response['main']['humidity'] >= 50:
        user_preferences['Weather'].append('humid')

    if user_preferences['Budget'] == []:
      user_preferences['Budget'] = [1000, 10000]

    if user_preferences['Review'] == "No":
      user_preferences['Review'] = None

    return user_preferences

  def add_new_destination(self, user_preferences):

    user_preferences = self.check_preferences(user_preferences)

    indian_cities[user_preferences['City']] = {
        'Weather' : user_preferences['Weather'],
        'Budget' : user_preferences['Budget'],
        'Review' : user_preferences['Review']
    }
    indian_cities = check_cities(indian_cities)
    return "New City Added !!"

  def recommend_destination(self, user_preferences):
      suggested_destinations = []
      suggested_destinations_temp = []

      review_city = None
      weather_city = []
      Budget_city = 0

      if user_preferences["City"] != "" and user_preferences["City"] in indian_cities.keys():
        review_city = indian_cities[user_preferences["City"]]["Review"]
        weather_city = indian_cities[user_preferences["City"]]["Weather"]
        Budget_city = (indian_cities[user_preferences["City"]]["Budget"][0] + indian_cities[user_preferences["City"]]["Budget"][1]) / 2

      if user_preferences["Budget"].isalpha() and user_preferences["Budget"].lower() == "no":
        user_preferences["Budget"] = 1e9
      else:
        user_preferences["Budget"] = float(user_preferences["Budget"])

      for key, values in indian_cities.items():
        flag=0
        flag_W = 0

        if key == user_preferences["City"]:
          continue

        weather = user_preferences["Weather"]
        if len(weather) == 0:
          flag = 1

        for w in weather:
          if w in values["Weather"]:
            flag += 1

        for w in weather_city:
          if w in values["Weather"]:
            flag_W += 1



        if user_preferences["Review"] != "No":
          if (flag != 0 or flag_W != 0) and ((similarity(user_preferences["Review"], values["Review"]) > 0.6) or (review_city and similarity(review_city, values["Review"])> 0.6)) and (budget_check(user_preferences["Budget"], values) or budget_check(Budget_city, values)):
            suggested_destinations_temp.append([key, max(flag, flag_W)])

        elif review_city:
          if flag_W != 0 and (budget_check(user_preferences["Budget"], values) or budget_check(Budget_city, values)) and similarity(review_city, values["Review"])> 0.6:
            suggested_destinations_temp.append([key, max(flag, flag_W)])
        else:
          if (flag != 0 or flag_W != 0) and (budget_check(user_preferences["Budget"], values) or budget_check(Budget_city, values)):
            suggested_destinations_temp.append([key, max(flag, flag_W)])

      suggested_destinations_temp = sorted(suggested_destinations_temp, key=lambda x: x[1], reverse=True)
      suggested_destinations = [x[0] for x in suggested_destinations_temp]
      return ", ".join(suggested_destinations)

def main():
  obj = Reccomendation_System()
  indian_cities = check_cities(indian_cities)
  print()
  print("Welcome to the Travel Recommendation System !!")
  while True:
    print("""

    Please select lines from menu:

    1. Recommed a place
    2. Add New Place
    3. Add Feedback to a Place
    4. Exit

    """)

    option = input("Enter the value: ")
    print()

    user_preferences = {"City": "",
                    "Weather": [],
                    "Budget": [],
                    "Review": ""}

    if option == "1":
      city = input("Would you like to enter city name for preferences: ").capitalize()
      weather = input("Enter the preferred weather condition for the place: ").lower().split(" ")

      while city == "No" and weather[0] == "no":
        weather = input("Please enter weather condition: ").lower().split(" ")

      budget = input("Enter Budget: ")
      review = input("Would you like to check feedback for a particular place: ")

      if city == "No":
        city = ""

      user_preferences['Weather'].extend(weather)
      user_preferences['City'] = city
      user_preferences['Budget'] = budget
      user_preferences['Review'] = review
      print("Suggested Travel Places: ", obj.recommend_destination(user_preferences))

    elif option == "2":

      city = input("Enter city name for preferences: ").lower().capitalize()
      weather = input("Enter the preferred weather condition for the place: ").lower().split(" ")
      budget = list(map(float, input("Enter Budget Range(lr hr): ").split(" ")))
      review = input("Would you like to check feedback for a particular place: ")

      user_preferences['Weather'].extend(weather)
      user_preferences['City'] = city
      user_preferences['Budget'].extend(budget)
      user_preferences['Review'] = review

      print(obj.add_new_destination(user_preferences))

    elif option == "3":

      city = input("Enter city name for preferences: ").lower().capitalize()

      if city not in indian_cities.keys():
        print("City not available, please add as new destination")
        continue

      review = input("Enter the Review: ")

      print(obj.add_feedback(review, city))

    elif option == "4":
      print("Exiting the Travel Recommendation System.")
      break
    else:
      print("Invalid option. Please choose a valid option (1/2/3/4).")

if __name__ == "__main__":
  main()