def calculate_probability_no_collisions():
    
    result = 1    
    for i in range(1,2450):
        result *= (1000000 - i)/1000000
    print(result)
        
    
def calculate_probability_no_collisions_2():
    
    constant = .999999
    result =1    
    for _ in range(3000025):
        result *= constant
    print(result)
    
calculate_probability_no_collisions()    # 0.049663
calculate_probability_no_collisions_2()  # 0.049785