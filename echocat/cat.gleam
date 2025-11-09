import gleam/option.{Option, Some, None}
import gleam/list
import gleam/string

// --- Core Types ---
type Cat {
  Cat(
    id: Int,
    name: String,
    species: String,
    age: Option(Int), // Age might be unknown
    weight_kg: Float,
    colors: List(CatColor),
    markings: List(Marking),
    eye_color: String,
    personality_traits: List(PersonalityTrait),
    health_status: HealthStatus,
    diet: Diet,
    vocalization: Vocalization,
    movement: MovementPattern,
  )
}

type CatColor {
  Black
  White
  Ginger
  Grey
  Calico
  Tabby
}

type Marking {
  Solid
  Striped
  Spotted
  Patched
  Pointed
}

type PersonalityTrait {
  Curious
  Aloof
  Affectionate
  Playful
  Territorial
  Skittish
  Vocal
}

type HealthStatus {
  Excellent
  Good
  Fair
  RequiresCare(vet_visits: List(String)) // Tracking vet appointments
}

type Diet {
  Diet(
    primary_food: String,
    treats: List(String),
    allergies: List(String),
    feeding_schedule: List(FeedingTime),
  )
}

type FeedingTime {
  Morning
  Evening
  Night
}

type Vocalization {
  Meow(frequency: Int)
  Purr(volume: Int)
  Chirp
  Hiss
  Silent
}

type MovementPattern {
  Stealthy
  Bouncy
  Lazy
  Erratic
}

// --- Constructor ---
pub fn create_cat(
  name: String,
  colors: List(CatColor),
  age: Option(Int),
) -> Cat {
  Cat(
    id: 0, // Would come from DB in real app
    name: name,
    species: "Felis catus",
    age: age,
    weight_kg: 4.2,
    colors: colors,
    markings: [Striped, Solid],
    eye_color: "Green",
    personality_traits: [Curious, Playful, Affectionate],
    health_status: Good,
    diet: Diet(
      primary_food: "Salmon kibble",
      treats: ["Tuna flakes", "Catnip"],
      allergies: [],
      feeding_schedule: [Morning, Evening],
    ),
    vocalization: Meow(frequency: 8),
    movement: Stealthy,
  )
}

// --- Behavioral Functions ---
pub fn describe(cat: Cat) -> String {
  let age_str = case cat.age {
    Some(years) -> string.inspect(years)
    None -> "unknown age"
  }
  
  let colors_str = cat.colors
    |> list.map(describe_color)
    |> string.join(", ")
  
  let traits_str = cat.personality_traits
    |> list.map(describe_trait)
    |> string.join(", ")
  
  "A " <> colors_str <> " cat named " <> cat.name <> 
  " (" <> age_str <> ").\nTraits: " <> traits_str <> 
  ".\nCommunicates with " <> describe_vocalization(cat.vocalization) <>
  " and moves with " <> describe_movement(cat.movement) <> " movements."
}

fn describe_color(color: CatColor) -> String {
  case color {
    Black -> "jet black"
    White -> "snow white"
    Ginger -> "vibrant ginger"
    Grey -> "slate grey"
    Calico -> "patchwork calico"
    Tabby -> "striped tabby"
  }
}

fn describe_trait(trait: PersonalityTrait) -> String {
  case trait {
    Curious -> "boundless curiosity"
    Aloof -> "regal independence"
    Affectionate -> "headbutting affection"
    Playful -> "pounce-happy playfulness"
    Territorial -> "guarded ownership"
    Skittish -> "nervous vigilance"
    Vocal -> "opinionated meowing"
  }
}

fn describe_vocalization(vocal: Vocalization) -> String {
  case vocal {
    Meow(freq) -> "frequent meows (" <> string.inspect(freq) <> "/10)"
    Purr(vol) -> "rumbling purrs (" <> string.inspect(vol) <> "/10)"
    Chirp -> "chirping trills"
    Hiss -> "defensive hisses"
    Silent -> "mysterious silence"
  }
}

fn describe_movement(move: MovementPattern) -> String {
  case move {
    Stealthy -> "silent stalking"
    Bouncy -> "springy bounces"
    Lazy -> "stretchy loafing"
    Erratic -> "sudden zoomies"
  }
}

// --- Usage Example ---
pub fn main() {
  let whiskers = create_cat("Whiskers", [Grey, White], Some(3))
  
  whiskers
  |> describe
  |> println
}