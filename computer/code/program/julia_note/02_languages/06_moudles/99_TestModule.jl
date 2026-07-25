module AnimalKingdom
export Animal, Mammal, Cat, Dog, speak # external interface.

abstract type Animal end
abstract type Mammal <: Animal end

struct Cat <: Mammal
    name::String
    weight::Float64
end

struct Dog <: Mammal
    name::String
    breed::String
end

speak(a::Animal) = println("Some generic animal sound")
speak(c::Cat) = println("$(c.name) says meow!")
end
