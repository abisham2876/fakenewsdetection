# =============================================================
# train_model.py — Train and save the Verifai ML model
# =============================================================
# Run ONCE before starting the Flask app:
#     python train_model.py
#
# Outputs:
#     model/model.pkl
#     model/vectorizer.pkl
# =============================================================

import os, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

os.makedirs("model", exist_ok=True)

# ── Training data ─────────────────────────────────────────────
real_news = [
    "Scientists at NASA confirmed the discovery of water ice on the Moon south pole",
    "The World Health Organization released new guidelines for managing respiratory infections",
    "The government announced a new infrastructure bill worth 1.2 trillion dollars to repair roads",
    "Stock markets fell sharply as investors reacted to rising inflation data from the Federal Reserve",
    "A new study published in Nature found that exercise reduces the risk of heart disease by 30 percent",
    "The United Nations Security Council held an emergency session to discuss the ongoing conflict",
    "Apple unveiled its latest iPhone lineup featuring improved camera and battery life",
    "Researchers at MIT developed a new solar panel material that improves energy conversion efficiency",
    "The Prime Minister addressed parliament on the economic recovery plan after the pandemic",
    "Global temperatures rose above pre-industrial levels according to climate scientists",
    "The central bank raised interest rates by 0.25 percent to combat rising consumer price inflation",
    "Local authorities confirmed injuries in a minor earthquake near the city last night",
    "Health officials urge citizens to get vaccinated before the flu season begins this winter",
    "A report by the International Monetary Fund projects 3.2 percent global economic growth",
    "The court sentenced the former official to five years in prison for corruption and embezzlement",
    "Scientists successfully landed a rover on Mars to study geological history and ancient life",
    "Parliament passed the climate change act requiring carbon emission reductions by 2035",
    "Doctors developed a new treatment method that reduces recovery time for pneumonia patients",
    "Electric vehicle sales rose by 40 percent in the first quarter compared to last year",
    "A peace agreement was signed between neighboring countries after months of diplomatic talks",
    "The aviation authority approved new safety regulations for commercial aircraft",
    "Researchers published findings showing a strong link between sleep deprivation and cognitive decline",
    "The mayor announced plans to build affordable housing units across the city over three years",
    "Police arrested three suspects in connection with the bank robbery investigation",
    "University researchers published new study on the effects of social media on mental health",
    "Hospital reports successful trial of new diabetes management drug with promising results",
    "Engineers completed construction of the new bridge spanning the river ahead of schedule",
    "Government launches new scholarship program for low-income undergraduate students",
    "Scientists warn that ocean acidification is threatening coral reef ecosystems worldwide",
    "City council approved the annual budget with increased spending on public education",
    "The central bank held its benchmark interest rate steady after reviewing economic indicators",
    "Authorities confirmed the wildfire is now 80 percent contained after days of firefighting efforts",
    "A new vaccine candidate entered phase three clinical trials with promising preliminary results",
    "The trade agreement between the two nations will eliminate tariffs on most goods by next year",
    "Researchers discovered a new species of deep-sea fish in the Pacific Ocean during a recent expedition",
]

fake_news = [
    "SHOCKING scientists secretly confirmed Earth is flat and NASA has been lying for decades share this",
    "BREAKING doctors HATE this one weird trick that cures cancer in just 3 days Big Pharma is hiding it",
    "Government putting microchips in vaccines to track and control the entire population share before deleted",
    "EXPOSED moon landing completely faked in Hollywood studio here is proof they do not want you to see",
    "This miracle fruit burns belly fat overnight doctors are furious that this secret got out try it now",
    "Anonymous insider reveals aliens are living among us and world leaders know about it but stay silent",
    "URGENT deep state is poisoning our water supply with chemicals to make people obedient and dumb",
    "Famous celebrity secretly arrested for running global underground criminal network media blackout",
    "SECRET CURE drinking this household liquid destroys all viruses instantly hospitals do not want you to know",
    "Billionaires created a weather machine to cause hurricanes and steal land from poor communities",
    "ALERT 5G towers are actually mind control devices designed to make you buy products and obey orders",
    "Scientists ADMIT they have been lying about climate change for 30 years to get more government funding",
    "Elite are harvesting children blood for secret youth serum whistleblower speaks out with proof",
    "BOMBSHELL elections completely rigged by secret society using invisible ink and fake ballot boxes",
    "Eating this one food every morning will make you immortal ancient secret suppressed by pharmaceutical companies",
    "CONFIRMED dinosaurs are still alive and the government is hiding them underground in Antarctica",
    "Real reason airlines dim cabin lights is to perform mind control experiments on passengers",
    "Doctors secretly confess all medicines are poison designed to keep you sick and dependent on the system",
    "LEAKED government documents prove historical wars were staged to reduce world population on purpose",
    "This man cured diabetes in 72 hours using kitchen ingredients medical establishment tried to silence him",
    "PROOF the sun is a giant artificial lamp controlled by secret civilization living inside the Earth",
    "Top scientist fired for revealing human DNA was engineered by extraterrestrials thousands of years ago",
    "Real virus is the mainstream media paid to keep you scared and under control by globalists wake up",
    "BREAKING world leader is actually a lizard person wearing a human suit video proof inside share now",
    "They are spraying chemtrails from planes to sterilize the population and no one is talking about this",
    "REVEALED government secretly replacing world leaders with robotic clones since 1980 insider confirms",
    "Doctors paid millions by secret cabal to suppress natural cure that eliminates all disease instantly",
    "MUST SHARE satellite images prove giant pyramid found underwater suppressed by elite institutions",
    "Banks stealing your money at night using secret algorithm only insiders know about wake up people",
    "Top virologist admits all pandemics manufactured by pharmaceutical companies for profit share now",
    "EXPOSED the water you drink contains mind-altering chemicals put there by the global elite since 1950",
    "Whistleblower reveals moon is actually a hollow artificial satellite built by an ancient civilization",
    "SHOCKING new study proves mobile phones emit radiation that turns people into obedient consumers",
    "Secret document leaked showing government planned every major natural disaster of the past 50 years",
    "Scientists suppressed for discovering plant extract that completely reverses aging in just two weeks",
]

texts  = real_news + fake_news
labels = [0] * len(real_news) + [1] * len(fake_news)

# ── Vectorise ─────────────────────────────────────────────────
print("=" * 50)
print("  Verifai — Model Training")
print("=" * 50)
print(f"\n Dataset: {len(texts)} examples  ({len(real_news)} real / {len(fake_news)} fake)")

vectorizer = TfidfVectorizer(
    max_features=8000,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True,
)
X = vectorizer.fit_transform(texts)

# ── Train ─────────────────────────────────────────────────────
print(" Training Logistic Regression...")
model = LogisticRegression(max_iter=1000, C=1.5, random_state=42)
model.fit(X, labels)

preds    = model.predict(X)
accuracy = accuracy_score(labels, preds)
print(f" Training accuracy: {accuracy * 100:.1f}%\n")
print(classification_report(labels, preds, target_names=["Real", "Fake"]))

# ── Save ──────────────────────────────────────────────────────
with open("model/model.pkl",      "wb") as f: pickle.dump(model, f)
with open("model/vectorizer.pkl", "wb") as f: pickle.dump(vectorizer, f)

print(" Saved: model/model.pkl")
print(" Saved: model/vectorizer.pkl")

# ── Quick sanity test ─────────────────────────────────────────
tests = [
    ("Scientists confirm new climate data published in peer-reviewed journal",           "real"),
    ("SHOCKING doctors hiding miracle cure that destroys all disease overnight share now", "fake"),
    ("Stock market rises as central bank holds interest rates steady this quarter",       "real"),
    ("Government putting microchips in vaccines to control the population wake up",       "fake"),
]
print("\n🔍 Sanity checks:")
for txt, expected in tests:
    v    = vectorizer.transform([txt])
    pred = model.predict(v)[0]
    prob = max(model.predict_proba(v)[0])
    got  = "fake" if pred == 1 else "real"
    ok   = "" if got == expected else ""
    print(f"  {ok} [{got} {prob*100:.0f}%] {txt[:60]}")

print("\n Done! Run:  python app.py")
print("=" * 50)
