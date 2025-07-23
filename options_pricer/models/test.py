from Black_Scholes import BlackScholes

Op1 = BlackScholes(82474,82300,0.098,0.15,1/365)

print(Op1.price("put"))