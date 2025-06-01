#Εισαγωγή της βιβλιοθήκης pyomo 
import pyomo.environ as pyo

#Δημιουργία του "αφηρημένου"/Abstract μοντέλου μας
model = pyo.AbstractModel(name = "cwk2_Aivanoulis")

#Δημιουργία των πινάκων και ορισμός των παραμέτρων 
model.Product=pyo.Set()
model.Gasoline=pyo.Set()

model.Cost_Barrel = pyo.Param(model.Product)
model.Octane_Rating = pyo.Param(model.Product)
model.Vapor_Pressure = pyo.Param(model.Product)
model.Supply = pyo.Param(model.Product)

model.Min_Octane_Rating = pyo.Param(model.Gasoline)
model.Max_Vapor_Pressure = pyo.Param(model.Gasoline)
model.Price_Barrel = pyo.Param(model.Gasoline)
model.Demand = pyo.Param(model.Gasoline)

#Δημιουργία Ν*Κ μεταβλητών για τις ποσότητες που αναμειγνύουμε όπου Ν τα index 
#του πίνακα Product και Κ τα index του Gasoline
model.X=pyo.Var(model.Product,model.Gasoline, within=pyo.NonNegativeReals)

#Δημιουργία μεταβλητών όσες και τα index του Product και Gasoline αντίστοιχα   
model.P2=pyo.Var(model.Product,within = pyo.NonNegativeReals)
model.G2=pyo.Var(model.Gasoline,within = pyo.NonNegativeReals)

#Δημιουργία της αντικειμενικής μας συνάρτησης 
def obj_rule(model):
    return(sum(model.G2[j]*model.Price_Barrel[j] for j in model.Gasoline)
    - sum(model.P2[i]*model.Cost_Barrel[i] for i in model.Product))
model.Obj = pyo.Objective(rule = obj_rule, sense=pyo.maximize)

#Δημιουργία περιορισμού απαίτησης παραγωγής Gasoline για διαφημιστικούς σκοπούς
def con_demand_rule(model,j):
    return(model.G2[j] >= model.Demand[j] )
model.con_demand = pyo.Constraint(model.Gasoline, rule = con_demand_rule)

#Δημιουργία του περιορισμού προμηθειών  
def con_c2_rule(model,i):
    return(model.P2[i]<=model.Supply[i])
model.con_c2= pyo.Constraint(model.Product, rule = con_c2_rule)

#Δημιουργία του περιορισμού για την κατηγοριοποίηση του τύπου βενζίνης με βάση 
#το Max Vapour pressure
def con_max_vapor_rule(model,j):
    return(sum(model.Vapor_Pressure[i] * model.X[i,j] for i in model.Product) <=
           model.Max_Vapor_Pressure[j]*sum(model.X[i,j] for i in model.Product))
model.con_max_vapor= pyo.Constraint(model.Gasoline, rule = con_max_vapor_rule)

#Δημιουργία περιορισμού για το σύνολο των ποσοτήτων που θα χρησιμοποιήσουμε απο
#κάθε υλικό
def con_product_rule(model,i):
    return(model.P2[i] == sum(model.X[i,j] for j in model.Gasoline))
model.con_product = pyo.Constraint(model.Product,rule=con_product_rule)

#Δημιουργία περιορισμού ποσοτήτων για τον κάθε τύπο βενζίνης που θα παραχθούν
def con_Gasoline_rule(model,j):
    return(model.G2[j] == sum(model.X[i,j] for i in model.Product))
model.con_Gasoline = pyo.Constraint(model.Gasoline,rule=con_Gasoline_rule)

#Δημιουργία του περιορισμού για την κατηγοριοποίηση του τύπου βενζίνης με βάση 
#το Min Octane rating
def con_min_oct_rule(model,j):
    return(sum(model.Octane_Rating[i] * model.X[i,j] for i in model.Product) >=
           model.Min_Octane_Rating[j]*sum(model.X[i,j] for i in model.Product))
model.con_min_oct= pyo.Constraint(model.Gasoline,rule = con_min_oct_rule)


    
    



