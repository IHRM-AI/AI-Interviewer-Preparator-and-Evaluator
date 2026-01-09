from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Neural network model banane ka function
# Input dimension batana padega kyunki har model ka input size different ho sakta hai
def build_model(input_dim):
    model = Sequential([
        # Pehla layer - 512 neurons, ReLU activation
        # Yeh input layer hai jo features ko process karega
        Dense(512, activation="relu", input_shape=(input_dim,)),
        
        # Doosra layer - 128 neurons, ReLU activation
        # Yeh hidden layer hai jo complex patterns dhundhega
        Dense(128, activation="relu"),
        
        # Output layer - sirf 1 neuron kyunki score predict karna hai
        # Sigmoid use kiya hai taaki output 0 aur 1 ke beech mein ho
        Dense(1, activation="sigmoid")
    ])
    
    # Model ko compile karo
    # Adam optimizer use kiya hai jo learning rate adjust karta hai automatically
    # MSE loss use kiya hai regression ke liye
    # MAE metric bhi track karega taaki performance dekh sakein
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"]
    )
    
    return model
