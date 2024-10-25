from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class GS1(DefinedNamespace):
    """
    GS1 vocabulary namespace elements

    Generated from: https://www.gs1.org/voc/data/gs1Voc.ttl
    Date: 2024-10-24
    """

    _NS = Namespace("https://ref.gs1.org/voc/")

    AI: URIRef  # A Data Type that corresponds to GS1 Application Identifiers defined in the GS1 General Specifications
    ALARM_CONDITION: URIRef  # Indicates the reporting of an alarm condition detected by a sensor device
    AbsoluteHumidity: URIRef  # The ratio of the mass of water vapour in a sample of moist air to the volume of the sample.  SI Units: kilogram per cubic metre
    AbsorbedDose: URIRef  # The energy absorbed per unit mass of the patient from the decay of a radionuclide given to a patient for diagnostic or therapeutic purposes.  SI Units: gray
    AbsorbedDoseRate: URIRef  # The energy absorbed per unit time per unit mass of the patient from the decay of a radionuclide given to a patient for diagnostic or therapeutic purposes.  SI Units: gray per second
    Acceleration: URIRef  # The rate of change of velocity, a vector quantity with magnitude and direction.  SI Units: metre per second per second
    AdditionalProductClassificationDetails: URIRef  # A product classification for the product other than the Global Product Classification(GPC brick value).
    AdditiveDetails: (
        URIRef  # A set of details about one of the additives within the product.
    )
    AllergenDetails: URIRef  # Details of an allergen for a product.
    AllergenTypeCode: URIRef
    AllergenTypeCode_1_2C3_BIS__282_2C4_DIAMINOPHENOXY_29PROPANE: URIRef  # Refers to the presence of 1,3-Bis-(2,4-diaminophenoxy)propane as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_1_NAPHTHOL: URIRef  # Refers to the presence of 1-Naphthol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_2_2C6_DIMETHOXY_3_2C5_PYRIDINEDIAMINE_HCL: URIRef  # Refers to the presence of 2,6-Dimethoxy-3,5-pyridinediamine HCl as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_2_HYDROXYETHYL_PICRAMIC_ACID: URIRef  # Refers to the presence of 2-Hydroxyethyl-picramic acid as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_2_METHYL_5_HYDROXYETHYLAMINOPHENOL: URIRef  # Refers to the presence of 2-Methyl-5-hydroxyethylaminophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_3_AMINO_2_2C4_DICHLOROPHENOL: URIRef  # Refers to the presence of 3-Amino-2,4-dichlorophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_3_AMINOPHENOL: URIRef  # Refers to the presence of 3-Aminophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_4_AMINO_3_NITROPHENOL: URIRef  # Refers to the presence of 4-Amino-3-nitrophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_4_HYDROXY_PROPYLAMINO_3_NITROPHENOL: URIRef  # Refers to the presence of 4-Hydroxy-propylamino-3-nitrophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_AA: URIRef  # Refers to the presence of Amylcinnamyl Alcohol in the product. - CAS Registry Number: 101-85-9 - Also known as: alpha-Amylcinnamyl alcohol - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABALONE: URIRef  # Refers to the presence of Abalone and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ABD: URIRef  # Refers to the presence of Tuna and its derivatives in the product. - Family/Genus/Species: Scombridae subfamily Scombrinae/(various) - Also known as: Albacore, Bigeye Tuna, Black Skipjack, Blackfin Tuna, Bluefin Tuna, Bullet Tuna, Buri, Dogtooth Tuna, Escolar, Frigate Tuna, Kawakawa, Little Tuna, Longtail Tuna, Pacific Bluefin Tuna, Skipjack Tuna, Slender Tuna, Southern Bluefin Tuna, Spotted Tunny, Tuna, Yellowfin Tuna - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABE: URIRef  # Refers to the presence of Walleye and its derivatives in the product. - Family/Genus/Species: Percidae/Sander/S. vitreus - Also known as: Walleye, Yellow Pike, Yellow Pickerel - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABF: URIRef  # Refers to the presence of Barnacles and its derivatives in the product. - Family/Genus/Species: (various) - Also known as: Barnacle, Goose Barnacle, Leaf Barnacle, Pico - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABG: URIRef  # Refers to the presence of Crab and its derivatives in the product. - Family/Genus/Species: Brachyura (various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABH: URIRef  # Refers to the presence of Crawfish and its derivatives in the product. - Family/Genus/Species: Astacidae or Cambaridae or Cambaroididae or Parastacidae/(various) - Also known as: Caribbean Spiny Lobster, Crawdad, Crawdaddy, Crawfish, Craydid, Crayfish, Freshwater Crayfish, Freshwater Lobsters, Marron, Mountain Lobsters, Mudbugs, Murray River Crayfish, Red Claw Crayfish, Red Swamp Crayfish, Rock Lobsters, Royal Spiny Lobster, White River Crayfish, Yabbie Crayfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABI: URIRef  # Refers to the presence of Krill and its derivatives in the product. - Family/Genus/Species:  Euphausiacea (various) - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABJ: URIRef  # Refers to the presence of Lobster and its derivatives in the product. - Family/Genus/Species: Nephropidae/(various) - Also known as: American Lobster, Blue Spiny Lobster, Blunt Slipper Lobster, Brazilian Slipper Lobster, California Spiny Lobster, Cape Spiny Lobster, Caribbean Lobsterette, Caribbean Spiny Lobster, Colorado Langostino, Common Spiny Lobster, Eastern Spiny Lobster, European Lobster, Flathead Locust Lobster, Florida Lobsterette, Gilchrist Spiny Lobster, Green Spiny Lobster, Hawaiian Spiny Lobster, Japanese Fan Lobster, Japanese Spiny Lobster, Lobsterette, Mud Spiny Lobster, Natal Spiny Lobster, Norway Lobster, Ornate Spiny Lobster, Painted Spiny Lobster, Pelagic Crab, Pink Spiny Lobster, Pronghorn Spiny Lobster, Red-banded Lobster, Ridged Slipper Lobster, Royal Spiny Lobster, Scalloped Spiny Lobster, Smoothtail Spiny Lobster, Southern Rock Lobster, Spanish Slipper Lobster, St. Paul Spiny Lobster, Swarming Squat Lobster, Urugavian Lobster, Western Red Lobster - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABK: URIRef  # Refers to the presence of Prawns and its derivatives in the product. Prawn is a common name for small aquatic crustaceans with an exoskeleton and ten legs (which is a member of the order decapoda), some of which can be eaten. The terms shrimp and prawn are common names, not scientific names. They are vernacular or colloquial terms which lack the formal definition of scientific terms. They are not taxa, but are terms of convenience with little circumscriptional significance. There is no reason to avoid using the terms shrimp or prawn when convenient, but it is important not to confuse them with the names or relationships of actual taxa. - Family/Genus/Species: (various) - Also known as: Banana Prawn, Brown Tiger Prawn, Caramote Prawn, Common Prawn, Eastern King Prawn, Giant Freshwater Prawn, Giant Gamba Prawn, Giant Tiger Prawn, Green Tiger Prawn, Indian Prawn, Jack-knife Prawn, Kuruma Prawn, Redtail Prawn, Roshna Prawn, Western King Prawn, Prawn - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABL: URIRef  # Refers to the presence of Shrimp and its derivatives in the product. The terms shrimp and prawn are common names, not scientific names. They are vernacular or colloquial terms which lack the formal definition of scientific terms. They are not taxa, but are terms of convenience with little circumscriptional significance. There is no reason to avoid using the terms shrimp or prawn when convenient, but it is important not to confuse them with the names or relationships of actual taxa. - Family/Genus/Species: (various) - Also known as: Akiami Paste Shrimp, Argentine Red Shrimp, Atlantic Seabob, Bigclaw River Shrimp, Blue Shrimp, Brown Rock Shrimp, Brown Shrimp, California Shrimp, Chinese White Shrimp, Cinnamon River Shrimp, Common Shrimp, Coonstriped Shrimp, Deep-water Rose Shrimp, Deep-water Rose Shrimp, Endeavour Shrimp, Golden Shrimp, Greasyback Shrimp, Humpy Shrimp, Jinga Shrimp, Kadal Shrimp, Kiddi Shrimp, Knife Shrimp, Kolibri Shrimp, Marsh Grass Shrimp, Northern Shrimp, Ocean Shrimp, Ohio Shrimp, Pink Shrimp, Pinkspotted Shrimp, Rainbow Shrimp, Royal Red Shrimp, Sakura Shrimp, Seven-spine Bay Shrimp, Sidestriped Shrimp, Smooth Nylon Shrimp, Southern Brown Shrimp, Southern White Shrimp, Speckled Shrimp, Spot Shrimp, Spot-tail Mantis Shrimp, Titi Shrimp, Western White Shrimp, White Shrimp, Whiteleg Shrimp, Tiger Shrimp, Shrimp - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ABN: URIRef  # Refers to the presence of Abalone and its derivates in the product. - Family/Genus/Species: Haliotidae/Haliotis/(various) - Also known as: Abalone, Ear Shells, Sea Ears, Muttonfish, Muttonshells, Ormer, Perlemoen, Pāua, Australian Abalone, Blackfoot Abalone, Blacklip Abalone, Flat Abalone, Giant Abalone, Green Abalone, Greenlip Abalone, Pink Abalone, Pinto Abalone, Pourtale Abalone, Red Abalone, Roe's Abalone, Threaded Abalone, Tube Abalone - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AC: URIRef  # Refers to the presence of Crustaceans and its derivates in the product - Family/Genus/Species: (Subphylum: Crustacea)/(various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ACP: URIRef  # Refers to the presence of Carp and its derivatives in the product. - Family/Genus/Species: Cyprinidae /Cyprinus/(various) - Also known as: Banded Carpet Shell, Bighead Carp, Black Carp, Blue Morwong, Carp, Common Carp, Crucian Carp, Giant Barb, Golden Carpet Shell, Grass Carp, Grooved Carpet Shell, Large Razorbelly Minnow, Mola Carplet, Mottled Grouper, Mrigal, Mud Carp, Quillback, Reba Carp, River Carpsucker, Rockfish, Rudd, Silver Carp, Small Scaled Mud Carp, Smooth Nylon Shrimp, Ziege - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AD: URIRef  # Refers to the presence of 3-Amino-2,4-dichlorophenol in the product. - CAS Registry Number: 61693-42-3 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADB: URIRef  # Refers to the presence of Bass and its derivatives in the product. - Family/Genus/Species: Percichthyidae Macquaria novemaculeata/Serranidae Centropristis striata/Nototheniidae Dissostichus eleginoides/Polyprionidae Stereolepis gigas - Also known as: Akamutsu, Antarctic Toothfish, Argentine Sea Bass, Atlantic Creolefish, Bank Sea Bass, Barred Sand Bass, Black Crappie, Black Sea Bass, Blackfin Seabass, Blackmouth Bass, Blacktip Grouper, Choctaw Bass, Common Name, European Sea Bass, European Seabass, Giant Perch, Giant Sea Bass, Guadalupe Bass, Hapuka, Himalayan Glassy Perchlet, Japanese SeabassLargemouth Bass, Japanese Seaperch, Kelp Bass, Largemouth Bass, Longtail Bass, Meagre, Murray Cod, Northern Rockfish, Oscar, Ozark Bass, Pacific Creolefish, Palmetto Bass, Patagonian Toothfish, Peacock Cichlid, Peruvian Sea Bass, Red Drum, Roanoke Bass, Rock Bass, Rock Sea Bass, Sea Bass, Shortfin Corvina, Smallmouth Bass, Splittail Bass, Spotted Bass, Spotted Grouper, Spotted Sand Bass, Striped Bass, Sunshine Bass, Suwannee Bass, Tripletail, Warmouth, White Bass, White Crappie, White Seabass, Wreckfish, Yellow Bass - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADC: URIRef  # Refers to the presence of Anchovies and its derivatives in the product. - Family/Genus/Species: Engraulidae/(various) - Also known as: Anchoveta, Anchovy, Bay Anchovy, Deepbody Anchovy, Dusky Anchovy, European Anchovy, Flat Anchovy, Japanese Anchovy, Key Anchovy, Moustached Thryssa, New Jersey Anchovy, Northern Anchovy, Ramcarat Grenadier Anchovy, Round Headed Anchovy, Silver Anchovy, Slough Anchovy, Southern Anchovy, Striped Anchovy, Teri Anchovy - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADE: URIRef  # Refers to the presence of Catfish and its derivatives in the product. - Family/Genus/Species: (various) - Also known as: Asian Redtail Catfish, Atlantic Wolffish, Bagrid Catfish, Bagrid Catfishes, Black Bullhead, Blue Catfish, Broadhead Catfish, Brown Bullhead, Catfish, Channel Catfish, Couma Sea Catfish, Crucifix Sea Catfish, Flathead Catfish, Flatwhiskered Catfish, Gafftopsail Catfish, Giant Catfish, Giant River Catfish, Gilded Catfish, Gillbacker Sea Catfish, Glass Catfishes, Hardhead Catfish, Hardhead Sea Catfish, Highwaterman Catfish, Hybrid Clarias Catfish, Large Spotted Dogfish, Long Whiskered Catfish, Mekong Giant Catfish, Northern Wolffish, Pabdah Catfish, Pemecou Sea Catfish, Sharptooth Catfish, Spotted Stargazer, Spotted Wolffish, Stinging Catfish, Striped Dwarf Catfish, Sucker Catfishes, Sutchi Catfish, Tiger Sorubim, Walking Catfish, Wels Catfish, White Catfish, Yaqui Catfish, Yellowtail Catfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADF: URIRef  # Refers to the presence of Cod and its derivatives in the product. - Family/Genus/Species: Gadidae/Gadus/(various) - Also known as: Arctic Cod, Atlantic Cod, Blue Antimora, Common Mora, Greenland Cod, Longfin Codling, Maori Cod, Northern Bastard Codling, Pacific Cod, Polar Cod, Red Cod, Rock Cod, Saffron Cod, Tadpole Mora, Toothed Cod - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADG: URIRef  # Refers to the presence of Flounder and its derivatives in the product. - Family/Genus/Species: Achiropsettidae or Bothidae or Pleuronectidae or Paralichthyidae or Samaridae/(various) - Also known as: Arctic Flounder, Arrowtooth Flounder, Bering Flounder, Bigmouth Flounder, Black Flounder, Blackback, Brill, Broad Flounder, California Flounder, Common Dab, Cortez Halibut, European Flounder, Eyed Flounder, Fivespot Flounder, Fluke, Fourspot Flounder, Fourspot Megrim, Greenback Flounder, Gulf Flounder, Indian Ocean Spiny Halibut, Kamchatka Flounder, Largetoothed Flounder, Longhead Dab, Megrim, Mexican Flounder, New Zealand Brill, Olive Flounder, Panther Flounder, Patagonian Flounder, Peacock Flounder, Pelican Flounder, Sand Flounder, Slime Flounder, Smalleye Flounder, Smalltoothed Flounder, Sohachi Flounder, Southern Flounder, Speckled Flounder, Starry Flounder, Summer Flounder, Three-eye Flounder, Threespot Righteye Flounder, Tropical Flounder, Windowpane, Winter Flounder, Witch, Witch Flounder, Yellowbelly Flounder, Yellowtail Flounder - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADH: URIRef  # Refers to the presence of Grouper and its derivatives in the product. - Family/Genus/Species: Serranidae subfamily Epinephelina/(various) - Also known as: Banded Grouper, Black Grouper, Blacktip Grouper, Bridled Grouper, Broomtail Grouper, Brownspotted Rockcod, Camouflage Grouper, Chevron Tailed Grouper, Comb Grouper, Comet Grouper, Coney, Coral Hind, Dot-dash Grouper, Dusky Grouper, Dusty Tail Grouper, Gag, Giant Grouper, Goliath, Graysby, Greasy Rockcod, Grouper, Gulf Coney, Gulf Grouper, Halfmoon Grouper, Hawaiian Grouper, Highfin Grouper, Hong Kong Grouper, Leopard Coralgrouper, Longspine Grouper, Malabar Grouper, Marbled Grouper, Misty Grouper, Mottled Grouper, Nassau Grouper, Netfin Grouper, Oblique-banded Grouper, Orange-spotted Grouper, Persian Grouper, Purplespotted Grouper, Red Grouper, Red Hind, Redmouth Grouper, Sabah Grouper, Sand Perch, Scamp, Sixbar Grouper, Slender Grouper, Snowy Grouper, Snubnose Grouper, Speckled Blue Grouper, Speckled Dwarf Grouper, Spinycheek Grouper, Spotted Grouper, Squaretail Coralgrouper, Starspotted Grouper, Star-studded grouper, Strawberry Hind, Striped Grouper, Tiger Grouper, Tomato Hind, Warsaw Grouper, Wavy Lined Grouper, White Grouper, White-blotched Grouper, Yellowedge Grouper, Yellow-edged Lyretail, Yellowfin Grouper, Yellowmouth Grouper - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADI: URIRef  # Refers to the presence of Haddock and its derivatives in the product. - Family/Genus/Species: Gadidae/Melanogrammus/Melanogrammus aeglefinus - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADJ: URIRef  # Refers to the presence of Hake and its derivatives in the product. - Family/Genus/Species: Merlucciidae or Phycidae or Gadidae subfamily Phycinae/(various) - Also known as: Argentine hake, Benguela hake, Brazilian Hake, Carolina Hake, Deep-water hake, European hake, Gayi hake, Gulf Hake, Longfin Hake, North Pacific hake, Offshore hake, Panama hake, Red Hake, Senegalese hake, Shallow-water hake, Silver hake, Southern Hake, Southern hake, Spotted Hake, White Hake - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADK: URIRef  # Refers to the presence of Halibut and its derivatives in the product. - FFamily/Genus/Species: Pleuronectidae/Hippoglossus/Hippoglossus hippoglossus or Hippoglossus stenolepis or Reinhardtius hippoglossoides - Also known as: Atlantic Halibut, Pacific Halibut, Greenland Halibut - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADL: URIRef  # Refers to the presence of Herring and its derivatives in the product. - Family/Genus/Species: Clupeidae/Clupea/(various) - Also known as: African Ilisha, Araucanian herring, Atlantic Herring, Atlantic Thread Herring, Bigeye Ilisha, Blackstripe herring, Blueback Herring, Day's round herring, Deepbody Thread Herring, Denticle herring, Dogtooth herring, Dwarf round herring, Flatiron Herring, Galapagos thread herring, Gilchrist's round herring, Graceful herring, Indian Ilisha, Indian Pellona, Javan Ilisha, Little-eye round herring, Middling thread herring, Pacific Flatiron herring, Pacific Herring, Pacific thread herring, Panamanian Ilisha, Pugnose Ilisha, Red-eye round herring, Round Herring, Sanaga pygmy herring, Silver Darlings, Silver-stripe round herring, Skipjack Herring, Slender thread herring, Striped herring, Tardoore, Toothed river herring, Two-finned round herring, Venezuelan herring, West African pygmy herring, Whitehead's round herring - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADM: URIRef  # Refers to the presence of Mahi Mahi and its derivatives in the product. - Family/Genus/Species: Coryphaenidae/Coryphaena/C. hippurus - Also known as: Mahi, Mahi-Mahi, Common Dolphinfish, Dorado, Pompano Dolphin - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADP: URIRef  # Refers to the presence of Pike and its derivatives in the product. - Family/Genus/Species: Esocidae/Esox/(various) - Also known as: Pike, Pickerel, American Pickerel, Amur Pike, Aquitanian Pike, Chain Pickerel, Muskellunge, Northern Pike, Southern Pike, Grass Pike - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADQ: URIRef  # Refers to the presence of Pollock and its derivatives in the product. - Family/Genus/Species: Gadidae/Pollachius/Pollachius pollachius or Pollachius virens - Also known as: Atlantic pollock, European pollock, Lieu Jaune, Lythe, Boston Blue, Silver Bill, Saithem Pollock, Pollack, Coley, Coalfish, Walleye Pollock - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADR: URIRef  # Refers to the presence of Salmon and its derivatives in the product. - Family/Genus/Species: Salmonidae subfamily Salmoninae/(various) - Also known as: Atlantic salmon, Chinook salmon, Chum salmon, Coho salmon, Masu salmon, Pacific Salmon, Pink salmon, Sockeye salmon - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADS: URIRef  # Refers to the presence of Snapper and its derivatives in the product. - Family/Genus/Species: Lutjanidae/(various) - Also known as: African Forktail Snapper, Amarillo Snapper, Black and White Snapper, Black Snapper, Blackfin Snapper, Blacktail Snapper, Bloodred Snapper, Blubberlip Snapper, Bluestriped Snapper, Cardinal Snapper, Caribbean Red Snapper, Chinamanfish, Colorado Snapper, Crimson Jobfish, Crimson Snapper, Cubera Snapper, Cunera Snapper, Dog Snapper, Emperor Snapper, Five-lined Snapper, Goldbanded Jobfish, Golden Snapper, Goldeneye Jobfish, Gold-striped Snapper, Gray Snapper, Green Jobfish, Humpback Snapper, John's Snapper, Lane Snapper, Lavender Jobfish, Mahogany Snapper, Malabar Snapper, Mangrove Red Snapper, Midnight Snapper, Mullet Snapper, Mutton Snapper, Oblique-banded Snapper, Onespot Snapper, Pacific Dog Snapper, Pacific Snapper, Pinjalo, Pink Snapper, Queen Snapper, Red Snapper, Rose Snapper, Ruby Snapper, Rufous Snapper, Rusty Jobfish, Saddleback Snapper, Sailfin Snapper, Sharptooth Jobfish, Silk Snapper, Smalltooth Jobfish, Snapper, Twinspot Snapper, Vermilion Snapper, Wenchman, Yellowstripe Snapper, Yellowtail Blue Snapper, Yellowtail Snapper - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADT: URIRef  # Refers to the presence of Sole and its derivatives in the product. - Family/Genus/Species: Soleidae or Achiridae or Cynoglossidae or Pleuronectidae/(various) - Also known as: American Sole, Butter Sole, C-O Sole, Curlfin Sole, Deepsea Sole, Double-lined Tonguesole, Dover Sole, English Sole, Fantail Sole, Flathead Sole, Hogchoker, Lemon Sole, Milky Spotted Sole, Mud Sole, Naked Sole, Narrowbanded Sole, New Zealand Lemon Sole, Northern Rock Sole, Oriental Sole, Pacific Dover, Petrale Sole, Rex Sole, Roughscale Sole, Sand Sole, Scrawled Sole, Senegalese Sole, Slender Sole, Sole, Solenette, Southern Rock Sole, Thickback Sole, Toungue Sole, Tounguefish, West Coast Sole, Yellowfin Sole - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADU: URIRef  # Refers to the presence of Swordfish and its derivatives in the product. - FFamily/Genus/Species: Xiphiidae/Xiphias/X. gladius - Also known as: Swordfish, Broadbill - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADV: URIRef  # Refers to the presence of Tilapia and its derivatives in the product. - Family/Genus/Species: Cichlidae/Talapia or Coptodon or Oreochormis or Sarotherodon/(various) - Also known as: Talapia, Mozambique Talapia, Nile Talapia, Blue Talapia - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ADW: URIRef  # Refers to the presence of Trout and its derivatives in the product. - Family/Genus/Species: Salmonida subfamily Salmoninae/Oncorhynchus or Salmo or Salvelinus- Also known as: Adriatic Trout, Alvord Cutthroat Trout, Apache Trout, Aurora Trout, Baja California Rainbow Trout, Beardslee Trout, Biwa Trout, Bonneville Cutthroat Trout, Brook Trout, Brown Trout, Bull Trout, Coastal Cutthroat Trout, Coastal Rainbow Trout (steelhead), Colorado River Cutthroat Trout, Columbia River Redband Trout, Crescenti Trout, Cutthroat Trout, Dolly Varden, Dolly Varden Trout, Eagle Lake Trout, Flathead Trout, Genus Oncorhynchus, Gila Trout, Golden Trout, Great Basin Redband Trout, Greenback Cutthroat Trout, Humboldt Cutthroat Trout, Inconnu, Kamchatkan Rainbow Trout, Kamloops Rainbow Trout, Kern River Rainbow Trout, Lacustrine Trout, Lahontan Cutthroat Trout, Lake Trout, Little Kern Golden Trout, Marble Trout, McCloud River Redband Trout, Mexican Golden Trout, Nelson's Trout, Ohrid Trout, Paiute Cutthroat Trout, Rainbow Trout, Rio Grande Cutthroat Trout, River Trout, Sacramento Golden Trout, San Pedro Martir Trout, Sea Trout, Sevan Trout, Sheepheaven Creek Redband Trout, Silver Trout, Snake River Fine-spotted Cutthroat Trout, Soca River Trout, Soča Trout, Speckled Lake (Splake) Trout, Tiger Trout, Trout, Westslope Cutthroat Trout, Whitehorse Basin Cutthroat Trout, Yellowstone Cutthroat Trout - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AE: URIRef  # Refers to the presence of eggs and its derivates in the product - Family/Genus/Species: - Also known as: Ovum - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AF: URIRef  # Refers to the presence of Fish and its derivates in the product. - Family/Genus/Species: (various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AH: URIRef  # Refers to the presence of Anise Alcohol in the product. - CAS Registry Number: 105-13-5 - Also known as: anisyl alcohol - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AI: URIRef  # Refers to the presence of Alpha-Isomethyl Ionone in the product. - CAS Registry Number: 127-51-5 - Also known as: 3 Methyl-4-(2,6,6-trimethyl-2-cyclohexen-1-yl)-3-buten-2-on - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AJF: URIRef  # Refers to the presence of Amberjack and its Derivatives in the product. - Family/Genus/Species: Carangidae/Seriola/(various) - Also known as: Amberjack, Buri, Greater amberjack, Lesser amberjack, Almaco jack, Yellowtail, Banded rudderfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AL: URIRef  # Refers to the presence of Amyl Cinnamal in the product. - CAS Registry Number: 122-40-7 - Also known as: alpha-amyl cinnamic aldehyde - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ALMONDS: URIRef  # Refers to the presence of almond and almond products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ALPHA_ISOMETHYL_IONONE: URIRef  # Refers to the presence of Alpha-Isomethyl Ionone as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_AM: URIRef  # Refers to the presence of milk and its derivatives in the product, as listed in in the product. - Family/Genus/Species: - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AMYLCINNAMYL_ALCOHOL: URIRef  # Refers to the presence of Amylcinnamyl Alcohol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_AMYL_CINNAMAL: URIRef  # Refers to the presence of Amyl Cinnamal as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_AN: URIRef  # Refers to the presence of Tree nuts or nuts and its derivatives in the product. - Family/Genus/Species: Fagales. - Also known as: Nuts - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ANCHOVY: URIRef  # Refers to the presence of anchovies and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ANISE_ALCOHOL: URIRef  # Refers to the presence of Anise Alcohol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ANO: URIRef  # Refers to the presence of Perch and its derivatives in the product. - Family/Genus/Species: Percidae subfamily Percinae/Perca/(various) - Also known as: Acadian Redfish, Argentinian Sandperch, Barred Surfperch, Black Surfperch, Blue Cod, Calico Surfperch, Chilean Sandperch, Climbing Perch, Deepwater Redfish, Eurasian Perch, Golden Perch, Golden Redfish, Grass Goby, Namorado Sandperch, Nile Perch, Norway Redfish, Pacific Ocean Perch, Painted Comber, Pile Perch, Redtail Surfperch, Rockfish, Rubberlip Seaperch, Sandperch, Sauger, Shiner Surfperch, Silver Perch, Striped Surfperch, Thicktail Cardinalfish, Volga Pikeperch, Walleye Surfperch, White Perch, Yellow Perch, Zander, Zebra Perch - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AP: URIRef  # Refers to the presence of Peanuts and its derivatives in the product. - Family/Genus/Species: Arachis hypogaea. - Also known as: Groundnut, Goober, Pindar, Monkey nut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_APL: URIRef  # Refers to the presence of Apple and its derivatives in the product. - Family/Genus/Species: Malus domestica. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AS: URIRef  # Refers to the presence of Sesame seeds or its derivatives in the product, as listed in in the product - Family/Genus/Species: Sesamum. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ASD: URIRef  # Refers to the presence of Aspartame and Aspartame-acesulfame salt in the product. - CAS Registry Number: 22839-47-0 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AU: URIRef  # Refers to the presence of sulfur dioxide and sulfits in the product. - CAS Registry Number: 7446-09-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AW: URIRef  # Refers to the presence of cereal grains containing gluten (protein) and their derivatives in the product. Includes wheat grains, grains that have been demonstrated capable of triggering celiac disease (such as common wheat, durum, spelt, khorasan, emmer and einkorn), barley, rye and oats as well as any cross hybrids of these grains (such as triticale). -Family/Genus/Species: Poaceae/Gramineae. - Also known as: Grasses, Grains. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AWF: URIRef  # Refers to the presence of Whitefish and its derivatives in the product. - Family/Genus/Species: (various) - Also known as: Humpback Whitefish, Lake Whitefish, Round Whitefish, Whitefish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_AY: URIRef  # Refers to the presence of Soybean and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Glycine max. - Also known as: Soya bean - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BA: URIRef  # Refers to the presence of Benzyl Alcohol in the product. - CAS Registry Number: 100-51-6 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BARLEY: URIRef  # Refers to the presence of Barley and barley products (gluten containing grain) as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BARNACLE: URIRef  # Refers to the presence of Barnacles and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BAS: URIRef  # Refers to the presence of Basa and its derivates in the product. - Family/Genus/Species: Pangasiidae/Pangasius/P. bocourti - Also known as: Basa, Basa Fish, Bocourti, Pangasius, Panga, Pacific Dory, River Cobbler, Swai - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BASA: URIRef  # Refers to the presence of Basa and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BASS: URIRef  # Refers to the presence of bass and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BB: URIRef  # Refers to the presence of Benzyl Benzoate in the product. - CAS Registry Number: 120-51-4 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BC: URIRef  # Refers to the presence of celery or its derivatives in the product, as listed in in the product. - Family/Genus/Species: Apium graveolens. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BE: URIRef  # Refers to the presence of 2 (4-tert-Butylbenzyl) in the product. - CAS Registry Number: 80-54-6 - Also known as: Butylphenyl Methylpropional - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BEECH_NUTS: URIRef  # Refers to the presence of Beech nuts [Fagus spp. (Fagaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BEEF: URIRef  # Refers to the presence of beef and its derivative in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BENZYL_ALCOHOL: URIRef  # Refers to the presence of Benzyl Alcohol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BENZYL_BENZOATE: URIRef  # Refers to the presence of Benzyl Benzoate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BENZYL_CINNAMATE: URIRef  # Refers to the presence of Benzyl Cinnamate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BENZYL_SALICYLATE: URIRef  # Refers to the presence of Benzyl Salicylate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BF: URIRef  # Refers to the presence of beef and its derivative in the product, in the product - Family/Genus/Species: Bos taurus Linnaeus - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BFD: URIRef  # Refers to the presence of Butterfish and its Derivatives in the product. - Family/Genus/Species: Stromateidae/Pampus or Peprilus or Stromateus/(various) - Also known as: Black Butterfish, Greenbone, Silver Pomfret, White Pomfret, Gulf Butterfish, Harvestfish, Pacific Pompano, Butterfish, Southwest Atlantic ButterfishCommon Name - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BFH: URIRef  # Refers to the presence of Bonito and its Derivatives in the product. - Family/Genus/Species: Scombridae subfamily: Scombrinae/Cybiosarda or Gymnosarda Gill or Orcynopsis Gill or Sarda/(various) - Also known as: Australian Bonito, Dogtooth Tuna, Leaping Bonito, Pacific Bonito, Plain Bonito, Striped Bonito - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BI: URIRef  # Refers to the presence of Benzyl Cinnamate in the product. - CAS Registry Number: 103-41-3 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BLF: URIRef  # Refers to the presence of Bluefish and its derivates in the product. - Family/Genus/Species: Pomatomidae/Pomatomus/P. saltatrix - Also known as: Bluefish, Elf, Shad, Tailor, Black Sea Bass, Shortfin Corvina, Opaleye, Rudderfish, Pollock - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BLUEFISH: URIRef  # Refers to the presence of Bluefish and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BM: URIRef  # Refers to the presence of Mustard or its derivatives in the product, as listed in in the product. - Family/Genus/Species: Brassicaceae. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BN: URIRef  # Refers to the presence of Isoeugenol in the product - CAS Registry Number: 97-54-1 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BND: URIRef  # Refers to the presence of Banana and its derivatives in the product. - Family/Genus/Species: Musa. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BO: URIRef  # Refers to the presence of d-Limonene in the product - CAS Registry Number: 5989-27-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BP: URIRef  # Refers to the presence of Linalool in the product - CAS Registry Number: 78-70-6 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BQ: URIRef  # Refers to the presence of Methyl 2-octynoate in the product - CAS Registry Number: 111-12-6 - Also known as: 2-Octynoic acid, methyl ester, Folione, Vert de violette, Methyl 2-octynate, Methyl pentylacetylenecarboxylate, NSC 72098, Methyl Heptin Carbonate, Methyl oct-2-ynoate - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BR: URIRef  # Refers to the presence of 1,3-Bis-(2,4-diaminophenoxy)propane in the product. - CAS Registry Number: 81892-72-0 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BRAZIL_NUTS: URIRef  # Refers to the presence of brazil nut and brazil nut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BRC: URIRef  # Refers to the presence of Barracuda and its Derivatives in the product. - Family/Genus/Species: Sphyraenidae/Sphyraena/(various) - Also known as: Pacific Barracuda, California Barracuda, Cuda, Barracouta, Barracuda, Great Barracuda, Short Barracuda, Picuda, Japanese Barracuda, Pickhandle Barracuda - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BREAM: URIRef  # Refers to the presence of Bream and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BRM: URIRef  # Refers to the presence of Bream and its derivates in the product. - Family/Genus/Species: Cyprinidae sub. Leuciscinae/(various) - Also known as: Antarctic Butterfish, Black Sweetlips, Bloodred Snapper, Bluegill, Blue-lined Large-eye Bream, Bogue, Bream, Bronze Bream, Carp Bream, Common Bream, Common Pandora, Delagoa Threadfin Bream, Fork-tailed Threadfin Bream, Freshwater Bream, Gilthead Bream, Golden Redfish, Golden Tai, Golden Threadfin Bream, Humpnose Big-eye Bream, Japanese Threadfin Bream, Longfin Tilapia, Long-spined Red Bream, Lowfinned Drummer, Madai, Malabar Snapper, Margate, Mauvelip Threadfin Bream, Mozambique Large-eye Bream, Pacific Pomfret, Pinfish, Pumpkinseed, Puntazzo, Red Bream, Red Porgy, Redbreast Tilapia, Redear Sunfish, River Bream, Rock Flagtail, Sea Bream, Southern Rays Bream, Squirefish, Taiwan Tai, Tarakihi, Threadfin Bream, Warmouth, Western Australian Gizzard Shad - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BS: URIRef  # Refers to the presence of Benzyl Salicylate in the product. - CAS Registry Number: 118-58-1 - Also known as: benzyl 2-hydroxybenzoate - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_BUTTERNUTS: URIRef  # Refers to the presence of Butternuts [Juglans cinerea (Juglandaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BUTYLPHENYL_METHYLPROPIONATE: URIRef  # Refers to the presence of Butylphenyl Methylpropionate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_BWD: URIRef  # Refers to the presence of buckwheat and its derivatives in the product. - Family/Genus/Species: Fagopyrum. - Also known as: Common buckwheat, Tartary buckwheat, Green buckwheat and Bitter buckwheat. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CA: URIRef  # Refers to the presence of Cinnamyl Alcohol in the product. - CAS Registry Number: 104-54-1 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CARP: URIRef  # Refers to the presence of Carp and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CARROTS: URIRef  # Refers to the presence of carrot and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_CASHEW_NUTS: URIRef  # Refers to the presence of cashew and cashew products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CATFISH: URIRef  # Refers to the presence of catfish and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CELERY: URIRef  # Refers to the presence of celery or their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_CEREALS_CONTAINING_GLUTEN: URIRef  # Refers to the presence of Cereals containing gluten and their derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_CFD: URIRef  # Refers to the presence of Cutlassfish and its Derivatives in the product. - Family/Genus/Species: Trichiuridae/(various) - Also known as: Black Scabbardfish, Silver Scabbardfish, Smallhead Hairtail, Atlantic Cutlassfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CFH: URIRef  # Refers to the presence of Croaker and its Derivatives in the product. - Family/Genus/Species: Sciaenidae/(various) - Also known as: Argentine Croaker, Atlantic Croaker, Bearded Jewfish, Belanger's Croaker, Bigtooth Corvina, Black Croaker, Blackmouth Croaker, Blackspotted Croaker, Blue Croaker, Bronze Croaker, Captainfish, Cob, Croceine Croaker, Donkey Croaker, Flathead Captainfish, Giant Captainfish, Gulf Corvina, Japanese Croaker, Meagre, Miiuy Croaker, Pama Croaker, Peruvian Croaker, Redlip Croaker, Reef Croaker, Shortfin Corvina, Shortfin Weakfish, Silver Croaker, Silver Croaker, Smalleye Croaker, Spotfin Croaker, Striped Croaker, Tigertooth Croaker, White Croaker, Whitemouth Drummer, Yellowfin Croaker, Donkey Croaker, Flathead Captainfish, Giant Captainfish, Gulf Corvina, Japanese Croaker, Meagre, Miiuy Croaker, Pama Croaker, Peruvian Croaker, Redlip Croaker, Reef Croaker, Shortfin Corvina, Shortfin Weakfish, Silver Croaker, Silver Croaker, Smalleye Croaker, Spotfin Croaker, Striped Croaker, Tigertooth Croaker, White Croaker, Whitemouth Drummer, Yellowfin Croaker - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CHAR: URIRef  # Refers to the presence of Char and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CHB: URIRef  # Refers to the presence of Chub and its derivates in the product. - Family/Genus/Species: Cyprinidae or Kyphosidae/(various) - Also known as: Atlantic Chub Mackerel, Bermuda Chub, Bigeye chub, Chum Salmon, Creek Chub, European chub, Fallfish, Flame chub, Flathead chub, Hornyhead chub, Kiyi, Lake chub, Largemouth Bass, Least chub, Leatherside chub, Oregon chub, Pacific Chub Mackerel, Ponto-Caspian chub, Rudderfish, Sea Chub, Slender chub, Spotted Chub Mackerel, Western chub, Yellow Chub - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CHESTNUTS: URIRef  # Refers to the presence of Chestnuts [Castanea spp. (Fagaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CHICKEN_MEAT: URIRef  # Refers to the presence of chicken meat and its derivative in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CHINQUAPINS: URIRef  # Refers to the presence of Chinquapins [Castanea pumila (Fagaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CHR: URIRef  # Refers to the presence of Char and its derivates in the product. - Family/Genus/Species: Salmonidae/Salmoninae/Salvelinus - Also known as: Char, Charr, Artic Char, Lake Char, Golden Char, Cole's Char, Coomsaharn Char, Gray's Char, Blunt-snouted Irish Char, Bear Island Char, Alsatian Char, Angayukaksurak Char, Boganida Char, Cherskii's Char, Chukot Char, Dryagin's Char, Kirikuchi Char, Lake Yessey Char, Long-finned Char, Sakhalinian Char, Small-mouth Char, Southern Dolly Varden Char, Taranets Char, White Char, Whitespotted Char, Yakutian Char - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CHUB: URIRef  # Refers to the presence of Chub and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CINNAMAL: URIRef  # Refers to the presence of Cinnamal as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CINNAMYL_ALCOHOL: URIRef  # Refers to the presence of Cinnamyl Alcohol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CISCO: URIRef  # Refers to the presence of Cisco and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CITRAL: URIRef  # Refers to the presence of Citral as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CITRONELLOL: URIRef  # Refers to the presence of Citronellol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CKF: URIRef  # Refers to the presence of Cusk and its Derivatives in the product. - Family/Genus/Species: Lotidae/Brosme/brosme - Also known as: Cusk, Tusk, Torsk, European Cusk, Brosmius - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CL: URIRef  # Refers to the presence of Cinnamal in the product. - CAS Registry Number: 104-55-2 - Also known as: cinnamaldehyde - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CLAM: URIRef  # Refers to the presence of Clam and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CLM: URIRef  # Refers to the presence of Clam and its derivates in the product. - Family/Genus/Species: (various) - Also known as: Alaska Razor, Arctic Surfclam, Asian Clam, Atlantic Geoduck, Atlantic Jackknife, Atlantic Razor, Atlantic Sanguin, Atlantic Surfclam, Banded Carpet Shell, Bent Surfclam, Bentnose Macoma, Butter Clam, Calico Clam, California Surfclam, California Tagelus, California Venus, Caribbean Winged Surfclam, Dish Surfclam, Fat Gaper, Flat Surfclam, Fragile Surfclam, Freshwater Clam, Frilled Venus, Golden Carpet Shell, Grand Razor Shell, Green Jackknife, Grooved Carpet Shell, Grooved Razor, Hard Clam, Hardshell Clam, Hatchet Surfclam, Hemphill Surfclam, Hen Clam, Hooked Surfclam, Jackknife Clam, Japanese Littleneck Clam, Littleneck Clam, Lyrate Hard Clam, Mogai Clam, New Zealand Wedge Clam, Northern Razor, Pacific Gaper, Pacific Geoduck, Pacific Littleneck Clam, Pipi Clam, Pismo Clam, Pod Razor, Razor Shell Clam, Rosy Jackknife, Shortneck Clam, Smooth Venus, Softshell Clam, Solid Sanguin Clam, Stout Tagelus, Sunray Venus, Sword Razor, Thin-shell Littleneck Clam, Washington Clam - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CM: URIRef  # Refers to the presence of chicken meat and its derivative in the product, in the product - Family/Genus/Species: Gallus domesticus - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CN: URIRef  # Refers to the presence of Citronellol in the product. - Family/Genus/Species: - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CO: URIRef  # Refers to the presence of Coumarin in the product. - Family/Genus/Species: - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_COCKLE: URIRef  # Refers to the presence of Cockle and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_COCOA: URIRef  # Refers to the presence of cocoa and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_COCONUTS: URIRef  # Refers to the presence of Coconuts [Cocos (Arecaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_COD: URIRef  # Refers to the presence of Cod and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_COK: URIRef  # Refers to the presence of Cockle and its derivates in the product. - Family/Genus/Species: Cardiidae/(various) - Also known as: Atlantic Giant Cockle, Bittersweet, Blood Cockle, California Cockle, Common Cockle, Decussate Bittersweet, Dock Cockle, Greenland Cockle, Knotted Cockle, New Zealand Cockle, Spiny Cockle, Violet Bittersweet - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CON: URIRef  # Refers to the presence of Conch and its derivates in the product. - Family/Genus/Species: Strombidae/(various) - Also known as: Conch, Florida Fighting Conch, Horse Conch, Milk Conch, Queen Conch, Spider Conch, West Indian Fighting Conch - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CONCH: URIRef  # Refers to the presence of Conch and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CORIANDER: URIRef  # Refers to the presence of coriander and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_CORN: URIRef  # Refers to the presence of corn and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_COTTON_SEEDS: URIRef  # Refers to the presence of Cotton Seeds or their derivatives in the product as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_COUMARIN: URIRef  # Refers to the presence of Coumarin as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CRAB: URIRef  # Refers to the presence of Crab and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CRAWFISH: URIRef  # Refers to the presence of Crawfish and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_CRUSTACEANS: URIRef  # Refers to the presence of Crustaceans and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_CS: URIRef  # Refers to the presence of Cotton Seeds or its derivatives in the product in the product - Family/Genus/Species: Gossypium. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CSC: URIRef  # Refers to the presence of Cisco and its derivates in the product. - Family/Genus/Species: Salmonidae/Coregonus/(various) - Also known as: Arctic Cisco, Bering Cisco, Blackfin Cisco, Bloater, Cisco, Deepwater Cisco, European Cisco, Irish pollan, Kiyi, Lake Cisco, Lake Herring, Least Cisco, Longjaw Cisco, Northern Cisco, Peled, Sardine Cisco, Shortjaw Cisco, Shortnose Cisco, Stechlin Cisco - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_CT: URIRef  # Refers to the presence of Citral in the product. - CAS Registry Number: 5392-40-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_D_LIMONENE: URIRef  # Refers to the presence of d-Limonene as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_DA: URIRef  # Refers to the presence of 2,6-Dimethoxy-3,5-pyridine diamine HCl in the product. - CAS Registry Number: 56216-28-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_DIAMINOPHENOLS: URIRef  # Refers to the presence of Diaminophenols as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_DMF: URIRef  # Refers to the presence of Drum and its Derivatives in the product. - Family/Genus/Species: Sciaenidae/(various) - Also known as: Banded Drum, Black Drum, Corb, Cubbyu, Freshwater Drum, Queenfish, Red Drum, Sand Drum, Spotted Drum, Star Drum, Totoaba - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_DP: URIRef  # Refers to the presence of Diaminophenol in the product. - CAS Registry Number: - Also known as: 137-09-7 - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_DYF: URIRef  # Refers to the presence of Dory and its Derivatives in the product. - Family/Genus/Species: (various) - Also known as: Black Oreo Dory, Buckler Dory, John Dory, Mirror Dory, Oreo, Silver Dory, Smooth Oreo Dory - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EEL: URIRef  # Refers to the presence of Eel and its derivates in the product. - Family/Genus/Species: (various) - Also known as: American Eel, Bandtooth Conger, Blackedge Cusk-eel, Blacktail Moray, Blacktail Pike-conger, Broadbanded Moray, Brown Moray, Conger Eel, Daggertooth Pike Conger, European Eel, Fangtooth Moray, Fawn Cusk-eel, Freckled Pike-conger, Giant Moray, Giant Snake Eel, Goldentail Moray, Green Moray, Hardtail Conger, Honey Comb Moray, Japanese Eel, Lesser Spiny Eel, Longfin Conger, Long-finned Eel, Manytooth Conger, Margintail Conger, Mottled Cusk-eel, Murray, Pebbletooth Moray, Reticulate Moray, Sea Eel, Short-finned Eel, Spiny Eel, Spotjaw Moray, Spotted Pike-conger, Stout Moray, Tiretrack Eel, Whiptail Conger, White Eel, Yellow Conger - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EG: URIRef  # Refers to the presence of Eugenol in the product. - CAS Registry Number: 97-53-0 - Also known as: clove oil - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EGGS: URIRef  # Refers to the presence of eggs and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_EOD: URIRef  # Refers to the presence of Escolar and its Derivatives in the product. - Family/Genus/Species: Gempylidae/Lepidocybium/flavobrunneum - Also known as: Escolar - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EP: URIRef  # Refers to the presence of Oakmoss extract in the product. - Family/Genus/Species: Evernia prunastri. - CAS Registry Number: 90028-68-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EUGENOL: URIRef  # Refers to the presence of Eugenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_EV: URIRef  # Refers to the presence of Treemoss extract in the product - Family/Genus/Species: Evernia Furfuracea - CAS Registry Number: 90028-67-4 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_EVERNIA_FURFURACEA: URIRef  # Refers to the presence of Evernia Furfuracea as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_EVERNIA_PRUNASTRI: URIRef  # Refers to the presence of Evernia Prunastri as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_FA: URIRef  # Refers to the presence of Farnesol in the product. - CAS Registry Number: 4602-84-0 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_FARNESOL: URIRef  # Refers to the presence of Farnesol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_FH: URIRef  # Refers to the presence of 4-Hydroxy-propyl amino-3-nitrophenol in the product. - CAS Registry Number: 92952-81-3 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_FISH: URIRef  # Refers to the presence of Fish and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_FLOUNDER: URIRef  # Refers to the presence of Flounder and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_FT: URIRef  # Refers to the presence of 4-Amino-3-nitrophenol in the product. - CAS Registry Number: 610-81-1 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GB: URIRef  # Refers to the presence of barley and its derivatives in the product. - Family/Genus/Species: Hordeum vulgare. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GE: URIRef  # Refers to the presence of Geraniol in the product. - CAS Registry Number: 106-24-1 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GERANIOL: URIRef  # Refers to the presence of Geraniol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_GINKGO_NUTS: URIRef  # Refers to the presence of Ginkgo nuts [Ginkgo biloba L. (Ginkgoaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_GK: URIRef  # Refers to the presence of kamut and its derivatives in the product. - Family/Genus/Species: Triticum turanicum. - Also known as: Khorasan wheat, Oriental wheat. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GL: URIRef  # Refers to the presence of Glutamate and its derivatives in the product. - Family/Genus/Species: - Also known as: Glutamic acid. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GLUTAMATE: URIRef  # Refers to the presence of glutamate and its derivative in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_GLUTEN: URIRef  # Refers to the presense of other gluten containing grain and gluten containing grain products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_GO: URIRef  # Refers to the presence of Oat and its derivatives in the product. - Family/Genus/Species: Avena sativa. - Also known as: Common oat. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GOM: URIRef  # Refers to the presence of Goat milk and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Capra - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GROUPER: URIRef  # Refers to the presence of Grouper and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_GS: URIRef  # Refers to the presence of Spelt and its derivatives in the product. - Family/Genus/Species: Pooideae/Triticum/T. spelta - Also known as: Spelt, Dinkel Wheat, Hulled Wheat - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_GTD: URIRef  # Refers to the presence of Gelatine in the product. - CAS Registry Number: 9000-70-8 - Also known as: Gelatin - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HADDOCK: URIRef  # Refers to the presence of Haddock and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HAKE: URIRef  # Refers to the presence of Hake and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HALIBUT: URIRef  # Refers to the presence of Halibut and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HAZELNUTS: URIRef  # Refers to the presence of hazelnut and hazelnut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HB: URIRef  # Refers to the presence of HC Blue No 12 in the product. - CAS Registry Number: 132885-85-9 - Also known as: 1-(alpha-hydroxyethyl)amino-2-nitro-4,N-ethyl-N-(alpha-​hydroxyethyl)aminobenzene - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HC: URIRef  # Refers to the presence of Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde in the product. - CAS Registry Number: 31906-04-4 - Also known as: Hydroxy-methylpentylcyclohexenecarboxaldehyde - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HC_BLUE_NO_11: URIRef  # Refers to the presence of HC Blue No 11 as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HC_BLUE_NO_12: URIRef  # Refers to the presence of HC Blue No 12 as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HD: URIRef  # Refers to the presence of HC Blue No 11 in the product. - CAS Registry Number: 23920-15-2 - Also known as: 2,2'-((4-((2-methoxyethyl)amino)-3-nitrophenyl)imino)diethanol - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HE: URIRef  # Refers to the presence of Hydroxybenzomorpholine in the product. - CAS Registry Number: 26021-57-8 - Also known as: 6-Hydroxybenzomorpholine - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HERRING: URIRef  # Refers to the presence of Herring and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HEXYL_CINNAMAL: URIRef  # Refers to the presence of Hexyl Cinnamal as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HH: URIRef  # Refers to the presence of Hydroxypropyl bis(N-hydroxyethyl-p-phenylenediamine) HCl in the product. - CAS Registry Number: 128729-28-2 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HICKORY_NUTS: URIRef  # Refers to the presence of hickory nuts [Carya spp. (Junglandacease)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HN: URIRef  # Refers to the presence of Hydroxyethyl-2-nitro-p-toluidine in the product. - CAS Registry Number: 100418-33-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HP: URIRef  # Refers to the presence of 2-Hydroxyethyl-picramic acid in the product. - CAS Registry Number: 99610-72-7 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HX: URIRef  # Refers to the presence of Hexyl Cinnamaldehyde in the product. - CAS Registry Number: 101-86-0 - Also known as: hexyl cinnamal - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HY: URIRef  # Refers to the presence of Hydroxycitronellal in the product. - CAS Registry Number: 107-75-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_HYDROXYBENZOMORPHOLINE: URIRef  # Refers to the presence of Hydroxybenzomorpholine as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HYDROXYCITRONELLAL: URIRef  # Refers to the presence of Hydroxycitronellal as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HYDROXYETHYL_2_NITRO_P_TOLUIDINE: URIRef  # Refers to the presence of Hydroxyethyl-2-nitro-p-toluidine as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_HYDROXYISOHEXYL_3_CYCLOHEXENE_CARBOXALDEHYDE_ISOEUGENOL_LIMONENE_LINAL: URIRef  # Refers to the presence of Hydroxyisohexyl 3-Cyclohexene Carboxaldehyde Isoeugenol Limonene Linal as listed in the regulations specified in AllergenSpecificationAgency and llergenSpecificationName.
    AllergenTypeCode_HYDROXYPROPYL_BIS_28N_HYDROXYETHYL_P_PHENYLDIAMINE_29_HCL: URIRef  # Refers to the presence of Hydroxypropyl bis(N-hydroxyethyl-p-phenyldiamine) HCl as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ISOEUGENOL: URIRef  # Refers to the presence of Isoeugenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_JCH: URIRef  # Refers to the presence of Japanese horse chestnuts and its derivatives in the product. - Family/Genus/Species: Aesculus turbinata. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_JFD: URIRef  # Refers to the presence of Jack and its Derivatives in the product. - Family/Genus/Species: (various) - Also known as: (Mix of fish in the 'jack' families) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_KAMUT: URIRef  # Refers to the presence of kamut and kamut products (glutencontaining grain) as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_KRILL: URIRef  # Refers to the presence of Krill and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_KWD: URIRef  # Refers to the presence of Kiwi and its derivatives in the product. - Family/Genus/Species: Actinidia. - Also known as: Chinese Gooseberry. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_LACTOSE: URIRef  # Refers to the presence of lactose as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_LAND: URIRef  # Refers to the presence of Land and sea snails (Escargot) and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_LGD: URIRef  # Refers to the presence of Lingcod and its Derivatives in the product. - Family/Genus/Species: Hexagrammidae/Ophiodon/elongatus - Also known as: Lingcod, Ling Cod, Buffalo cod, Cultus cod - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_LICHEE_NUTS: URIRef  # Refers to the presence of Lichee nuts [Litchi chinensis Sonn. (Sapindaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_LIMPETS: URIRef  # Refers to the presence of Limpets and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_LINALOOL: URIRef  # Refers to the presence of Linalool as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_LMT: URIRef  # Refers to the presence of Limpets and its derivates in the product. - Family/Genus/Species: Patellogastropoda (various) - Also known as: Hoof Snail, Keyhole Limpet, Keyhole Limpte, Lake Limpet, Limpet, Limpets, Owl Limpet, Plant Limpet, Purple Keyhole Limpet, Rayed Mediterranean Limpet, Rough Keyhole Limpet, Rver Limpet, Slipper Snail, Slit Limpet, Umbrella Slugs - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_LOBSTER: URIRef  # Refers to the presence of Lobster and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_LSN: URIRef  # Refers to the presence of Land and sea snails (Escargot) and its derivates in the product. - Family/Genus/Species: Gastropoda (various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_LUPINE: URIRef  # Refers to the presence of Lupine and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_LX: URIRef  # Refers to the presence of latex in the product. - CAS Registry Number: 9006-04-6 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MAC: URIRef  # Refers to the presence of Mackerel and its derivates in the product. - Family/Genus/Species: Acanthocybium or Grammatorcynus or Rastrelliger or Scombridae or Scomberomorus/(various) - Also known as: Atka Mackerel, Atlantic Mackerel, Atlantic Sierra, Atlantic Spanish Mackerel, Australian Spotted Mackerel, Blue Mackerel, Broadbarred King Mackerel, Butterfly Mackerel, Cero, Cero Mackerel, Chinese Mackerel, Double-lined Mackerel, Gulf Sierra, Indian Mackerel, Indo-Pacific king Mackerel, Island Mackerel, Japanese Seer, Japanese Spanish Mackerel, King Mackerel, Korean Mackerel, Monterey Spanish Mackerel, Narrow-barred Mackerel, Narrow-barred Spanish Mackerel, Pacific Sierra, Papuan Spanish Mackerel, Queen Mackerel, Queensland School Mackerel, Serra Spanish Mackerel, Shark Mackerel, Short Mackerel, Spanish Mackerel, Spotted Seerfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MACADAMIA_NUTS: URIRef  # Refers to the presence of macadamia nut and macadamia nut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_MACKEREL: URIRef  # Refers to the presence of Mackerel and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_MAHI_MAHI: URIRef  # Refers to the presence of Mahi Mahi and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_MAL: URIRef  # Refers to the presence of Marlin and its derivates in the product. - Family/Genus/Species: Istiophoridae/(various) - Also known as: Atlantic Blue Marlin, Atlantic Sailfish, Black Marlin, Indo-Pacific Blue Marlin, Indo-Pacific Sailfish, Longbill Spearfish, Mediterranean Spearfish, Roundscale Spearfish, Shortbill Spearfish, Striped Marlin, White Marlin - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MARLIN: URIRef  # Refers to the presence of Marlin and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_MELATONIN: URIRef  # Refers to the presence of Melatonin, a hormone secreted by the pineal gland that inhibits melanin formation and is thought to be concerned with regulating the reproductive cycle.
    AllergenTypeCode_METHYL_2_OCTYNOATE: URIRef  # Refers to the presence of Methyl 2-Octynoate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_METHYL_HEPTIN_CARBONATE: URIRef  # Refers to the presence of Methyl heptin carbonate as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_MFD: URIRef  # Refers to the presence of Milkfish and its Derivatives in the product. - Family/Genus/Species: Chanidae/Chanos/chanos - Also known as: False Trevalliesm Milkfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MH: URIRef  # Refers to the presence of 2-Methyl-5-hydroxyethylaminophenol in the product. - CAS Registry Number: 55302-96-0 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MILK: URIRef  # Refers to the presence of milk and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_MKF: URIRef  # Refers to the presence of Monkfish (Anglerfish, Lotte) and its derivates in the product. - Family/Genus/Species: Lophiidae/Lophius/(various) - Also known as: American Angler, Angler, Anglerfish, Blackbellied Angelr, Blackfin Goosefish, Blackfin Monkfish, Devil Angelfish, Fishing-Frogs, Frog-Fish, Goosefish, Monkfish, Sea-Devils, Shortspine African Angelr, Yellow Goosefish, Yellow Goosfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ML: URIRef  # Refers to the presence of lactose in the product. - Family/Genus/Species: - Also known as: Milk sugar, Lactobiose, 4-O-β-D-Galactopyranosyl-D-glucose - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MM: URIRef  # Refers to the presence of Melatonin, a hormone secreted by the pineal gland that inhibits melanin formation and is thought to be concerned with regulating the reproductive cycle. - CAS Registry Number: 73-31-4 - Also known as: N-acetyl-5-methoxy tryptamine - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MMD: URIRef  # Refers to the presence of Matsutake mushroom and its derivatives in the product. - Family/Genus/Species: Tricholoma matsutake. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MOD: URIRef  # Refers to the presence of Mango and its derivatives in the product. - Family/Genus/Species: Mangifera. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MOLLUSCS: URIRef  # Refers to the presence of molluscs and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_MONKFISH__28ANGLERFISH_2C_LOTTE_29: URIRef  # Refers to the presence of Monkfish (Anglerfish, Lotte) and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_MSS: URIRef  # Refers to the presence of Mussels and its derivates in the product. - Family/Genus/Species: (various) - Also known as: American Angler, Bearded Horse Mussel, Blue Mussel, California Mussel, Chilean Mussel, Cholga Mussel, Mediterranean Mussel, Mussel, New Zealand Green Mussel, Northern Horse Mussel - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_MUSSELS: URIRef  # Refers to the presence of Mussels and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_MUSTARD: URIRef  # Refers to the presence of mustard or their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_NC: URIRef  # Refers to the presence of cocoa and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Theobroma cacao. - Also known as: Cacao. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NE: URIRef  # Refers to the presence of Peas and its derivatives in the product. - Family/Genus/Species: Pisum sativum. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NK: URIRef  # Refers to the presence of coriander and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Coriandrum sativum. - Also known as: Chinese parsley, Dhania and Cilantro. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NL: URIRef  # Refers to the presence of Lupine and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Lupinus. - Also known as: Lupin and Bluebonnet. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NM: URIRef  # Refers to the presence of corn and its derivatives in the product. - Family/Genus/Species: Zea mays. - Also known as: Maize. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NO_DECLARED_ALLERGENS: URIRef  # Does not contain declaration obligatory allergens as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_NP: URIRef  # Refers to the presence of Pod fruits and its derivates in the product. - Family/Genus/Species: Fabaceae - Also known as: Legume. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NR: URIRef  # Refers to the presence of Rye and its derivatives in the product. - Family/Genus/Species: Secale cereale. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_NW: URIRef  # Refers to the presence of carrot and its derivates in the product. - Family/Genus/Species: Daucus carota subsp. sativus. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_OAT: URIRef  # Refers to the presence of oat and oat products (gluten containing grain) as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_OCT: URIRef  # Refers to the presence of Octopus and its derivates in the product. - Family/Genus/Species: Octopus - Also known as: Octopus, Giant Octopus, Veined Octopus, Common Octopus - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_OCTOPUS: URIRef  # Refers to the presence of Octopus and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_OFD: URIRef  # Refers to the presence of Oilfish and its Derivatives in the product. - Family/Genus/Species: Gempylidae/Ruvettus/pretiosus - Also known as: Oilfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_OGD: URIRef  # Refers to the presence of Orange and its derivatives in the product. - Family/Genus/Species: Rutaceae. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ON: URIRef  # Refers to the presence of 1-Naphthol in the product. - CAS Registry Number: 90-15-3 - Also known as: α-naphthol - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ORANGE_ROUGHY: URIRef  # Refers to the presence of Orange roughy and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ORR: URIRef  # Refers to the presence of Orange roughy and its derivates in the product. - Family/Genus/Species: Trachichthyidae/Hoplostethus/H. atlanticus - Also known as: Orange Roughy, Red Roughy, Alimehead, Deep Sea Perch - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_OYS: URIRef  # Refers to the presence Oysters and its derivates in the product. - Family/Genus/Species: Ostreidae or Pteriidae/(various) - Also known as: Chilean Oyster, Eastern Oyster, Edible Oyster, European Flat Oyster, Kumamoto Oyster, New Zealand Dredge Oyster, New Zealand Rock Oyster, Olympia Oyster, Pacific Oyster, Portuguese Oyster, Sydney Rock Oyster, Tautog - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_OYSTERS: URIRef  # Refers to the presence Oysters and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_P_METHYLAMINOPHENOL: URIRef  # Refers to the presence of p-Methylaminophenol as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_P_PHENYLENEDIAMINE: URIRef  # Refers to the presence of p-Phenylenediamine in the product as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PEANUTS: URIRef  # Refers to the presence of peanuts and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_PEAS: URIRef  # Refers to the presence of peas and pea products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PECAN_NUTS: URIRef  # Refers to the presence of pecan nut and pecan nut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PER: URIRef  # Refers to the presence of Periwinkle and its derivates in the product. - Family/Genus/Species: Littorina. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PERCH: URIRef  # Refers to the presence of Perch and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PERIWINKLE: URIRef  # Refers to the presence of Periwinkle and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PFD: URIRef  # Refers to the presence of Puffer and its Derivatives in the product. - Family/Genus/Species: Tetraodontidae/(various) - Also known as: Balloonfish, Bandtail Puffer, Blowfish, Blowies, Blunthead Puffer, Bubblefish, Bullseye Puffer, Checkered Puffer, Common Puffers, Globefish, Honey toads, Least Puffer, Longnose Puffer, Marbled Puffer, Moontail Blassop, Northern Puffer, Oceanic Puffer, Pufferfish, Puffers, Sea squab, Sharpnosed Puffers, Smooth Puffer, Southern Puffer, Sugar toads, Swellfish, Toadfish, Toadies - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PGT: URIRef  # Refers to the presence of Patagonian Toothfish and its Derivatives in the product. - Family/Genus/Species: Nototheniidae/Dissostichus/eleginoides - Also known as: Patagonian Toothfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PHD: URIRef  # Refers to the presence of Peach and its derivatives in the product. - Family/Genus/Species: Prunus persica. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PIKE: URIRef  # Refers to the presence of Pike and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PILI_NUTS: URIRef  # Refers to the presence of Pili nuts [Canarium ovatum (Burseraceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PINE_NUTS: URIRef  # Refers to the presence of Pine Nuts and their derivatives as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PISTACHIOS: URIRef  # Refers to the presence of pistachio and pistachio products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PLAICE: URIRef  # Refers to the presence of Plaice and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PLC: URIRef  # Refers to the presence of Plaice and its derivates in the product. - Family/Genus/Species: Pleuronectidae/(various) - Also known as: American Plaice, Alaskan Plaice, European Plaice, Scale-eye Plaice, Summer Plaice - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PM: URIRef  # Refers to the presence of p-Methylaminophenol in the product. - CAS Registry Number: 55-55-0 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PN: URIRef  # Refers to the presence of Pine nuts and its derivatives in the product. - Family/Genus/Species: Pinus. - Also known as: Pine seeds. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PO: URIRef  # Refers to the presence of Pork and its derivative in the product, in the product - Family/Genus/Species: - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_POD_FRUITS: URIRef  # Refers to the presence of pod fruits and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_POLLOCK: URIRef  # Refers to the presence of Pollock and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_POM: URIRef  # Refers to the presence of Pompano and its derivates in the product. - Family/Genus/Species: Carangidae subfamily Trachinotinae/Trachinotus/(various) - Also known as: African Pompano, Blackblotch Pompano, Cayenne Pompano, Derbio, Florida Pompano, Florida Pompano, Gafftopsail Pompano, Gafftopsail Pompano, Guinean Pompano, Indian Pompano, Largespotted Dart, Longfin Pompano, Marquesas Dart, Oyster Pompano, Paloma Pompano, Paloma Pompano, Palometa, Palometa, Palometta Permit, Permit, Permit, Plata Pompano, Pompano, Shortfin Pompano, Smallspotted Dart, Snubnose Pompano, Snubnose Pompano, Southern Pompano, Steel Pompano, Swallowtail Dart - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_POMPANO: URIRef  # Refers to the presence of Pompano and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_POPPY_SEEDS: URIRef  # Refers to the presence of Poppy Seeds or their derivatives in the product as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PORGY: URIRef  # Refers to the presence of Porgy and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PORK: URIRef  # Refers to the presence of pork and its derivative in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PP: URIRef  # Refers to the presence of p-Phenylenediamine in the product in the product. - CAS Registry Number: 106-50-3 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PRAWNS: URIRef  # Refers to the presence of Prawns and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_PRG: URIRef  # Refers to the presence of Porgy and its derivates in the product. - Family/Genus/Species: Sparidae/(various) - Also known as: Dentex, Grass Porgy, Longspine Porgy, Madai, Panga, Pinfish, Porgy, Puntazzo, Red Porgy, River Bream, Scup, Sea Bream, Sheepshead, Silver Porgy, Spotted Pinfish, Squirefish, Whitebone Porgy - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PS: URIRef  # Refers to the presence of Poppy seeds or its derivatives in the product in the product. - Family/Genus/Species: Papaver somniferum. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_PULSES: URIRef  # Refers to the presence of pulses. An annual leguminous crop yielding from one to twelve seeds of variable size, shape, and colour within a pod. Pulses are used for food and animal feed. The term 'pulse', as used by the Food and Agricultural Organization (FAO), is reserved for crops harvested solely for the dry seed. This excludes green beans and green peas, which are considered vegetable crops. Also excluded are crops that are mainly grown for oil extraction
    AllergenTypeCode_QUA: URIRef  # Refers to the presence of Quahaugs and its derivates in the product. - Family/Genus/Species: Veneridae/Mercenaria/M. mercenaria - Also known as: Cherrystones, Chowder Clams, Countnecks, Quahog, Quahaug, Hard-shell Clam, Ocean Quahog, Peanut Clam, Round Clam, Topnecks, Southern Quahog - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_QUAHAUGS: URIRef  # Refers to the presence of Quahaugs and its derivatives in the product, listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_QUEENSLAND_NUTS: URIRef  # Refers to the presence of queensland nut and queensland nut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ROCKFISH: URIRef  # Refers to the presence of Rockfish and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_ROF: URIRef  # Refers to the presence of Rockfish and its derivates in the product. Rockfish is a common term for several species of fish, referring to their tendency to hide among rocks. - Family/Genus/Species: (various) - Also known as: Aurora Rockfish, Bank Rockfish, Black & Yellow Rockfish, Black Rockfish, Blackgill Rockfish, Blue Rockfish, Bocaccio, Bronzespotted Rockfish, Brown Rockfish, Calico Rockfish, Canary Rockfish, Chameleon Rockfish, Chilipepper (Fish), China Rockfish, Copper Rockfish, Cowcod, Darkblotched Rockfish, Dusky Rockfish, Dwarf-red Rockfish, Flag Rockfish, Freckled Rockfish, Gopher Rockfish, Grass Rockfish, Greenblotched Rockfish, Greenspotted Rockfish, Greenstriped Rockfish, Halfbanded Rockfish, Harlequin Rockfish, Honeycomb Rockfish, Kelp Rockfish, Mexican Rockfish, Northern Rockfish, Olive Rockfish, Pink Rockfish, Pinkrose Rockfish, Puget Sound Rockfish, Pygmy Rockfish, Quillback Rockfish, Red Rockfish, Redbanded Rockfish, Redstripe Rockfish, Rockfish, Rosethorn Rockfish, Rosy Rockfish, Rougheye Rockfish, Semaphore Rockfish, Sharpchin Rockfish, Shortbelly Rockfish, Shortraker Rockfish, Silvergray Rockfish, Speckled Rockfish, Splitnose Rockfish, Squarespot Rockfish, Starry Rockfish, Stripetail Rockfish, Swordspine Rockfish, Tiger Rockfish, Treefish, Vermilion Rockfish, Widow Rockfish, Yelloweye Rockfish, Yellowmouth Rockfish, Yellowtail Rockfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_RYE: URIRef  # Refers to the presence of rye and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_SA: URIRef  # Refers to the presence of almonds and its derivatives in the product. - Family/Genus/Species: Prunus dulcis. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SAD: URIRef  # Refers to the presence of Sapucaia nuts and its derivatives in the product. - Family/Genus/Species: Lecythis zabucajo. - Also known as: paradise nut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SALICYLATE: URIRef  # Refers to the presence of Salicylate, a salt or ester of salicylic acid.
    AllergenTypeCode_SALMON: URIRef  # Refers to the presence of Salmon and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SAR: URIRef  # Refers to the presence of Sardine and its derivates in the product. - Family/Genus/Species: Clupeidae/(various) - Also known as: Australian Pilchard, European Pilchard, Japanese Pilchard, Pacific Sardine, South African Pilchard, False Pilchard, Fringescale Sardinella, Japanese Scaled Sardine, Oil Sardine, Orangespot Sardine, Perforated-scale Sardine, Redear Sardine, Scaled Sardine, Spanish Sardine, White Sardine - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SARDINE: URIRef  # Refers to the presence of Sardine and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SB: URIRef  # Refers to the presence of Seed products and its derivatives in the product - Family/Genus/Species: - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SC: URIRef  # Refers to the presence of Cashews and its derivatives in the product. - Family/Genus/Species: Anacardium occidentale. - Also known as: Cashew nut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SCA: URIRef  # Refers to the presence of Scallops and its derivates in the product. - Family/Genus/Species: Pectinidae/Pecten/(various) - Also known as: Atlantic Calico Scallop, Atlantic Scallop, Australian Scallop, Bay Scallop, Common Japanese Scallop, Farrer's Scallop, Giant Scallop, Great Scallop, Iceland Scallop, Lined Scallop, New Zealand Commercial Scallop, Nucleus Scallop, Pacific Calico Scallop, Paper Scallop, Patagonian Scallop, Peruvian Calico Scallop, Peruvian Scallop, Queen Scallop, Reddish Scallop, Red-ribbed Scallop, San Diego Scallop, Scallop, Scallop Saucer, Sea Scallop, Southern Queen Scallop, Southern Scallop, Spiny Scallop, Thailand Moon scallop, Weathervane Scallop, White Scallop, Zigzag Scallop - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SCALLOPS: URIRef  # Refers to the presence of Scallops and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SD: URIRef  # Refers to the presence of beech nuts and its derivatives in the product. - Family/Genus/Species: Fagus. - Also known as: Beech mast. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SDF: URIRef  # Refers to the presence of Scad fish and its derivatives in the product. - Family/Genus/Species: Carangidae (order Perciformes) - Also known as: Mackerel Scad, Amberjack Scad, Jack Scad..etc.- Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SE: URIRef  # Refers to the presence of butternuts and its derivatives in the product. - Family/Genus/Species: Juglans cinerea. - Also known as: White walnut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SEED_PRODUCTS: URIRef  # Refers to the presence of seed products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_SESAME_SEEDS: URIRef  # Refers to the presence of sesame seeds or their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_SF: URIRef  # Refers to the presence of Chinquapins and its derivatives in the product. - Family/Genus/Species: Castanea pumila. - Also known as: Allegheny chinquapin, American chinquapin and Dwarf Chetsnut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SFD: URIRef  # Refers to the presence of Swai and its Derivatives in the product. - Family/Genus/Species: Pangasiidae/Pangasianodon/hypophthalmus - Also known as: Sutchi Catfish, Swai, Sutchi, Striped Pangasius, Tra - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SFT: URIRef  # Refers to the presence of Spinefoot and its Derivatives in the product. - Family/Genus/Species: Siganidae/Siganus/(various) - Also known as: Bluespotted Spinefish, Foxface, Pearly Spinefoot, Rabbitfish, Streaked Spinefoot, Spinefoot - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SG: URIRef  # Refers to the presence of Ginkgo nuts and its derivatives in the product. - Family/Genus/Species: Ginkgo. - Also known as: Ginkgo seeds, Gingko. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SH: URIRef  # Refers to the presence of Hazelnuts and its derivatives in the product. - Family/Genus/Species: Corylus. - Also known as: Cobnuts, Filberts. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SHARK: URIRef  # Refers to the presence of Shark and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SHD: URIRef  # Refers to the presence of Sheephead and its Derivatives in the product. - Family/Genus/Species: Labridae/Semicossyphus/darwini or pulcher or reticulatus - Also known as: Sheephead, California Sheephead, Galápagos sheephead, Goldspot sheepshead, Asian sheepshead wrasse - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SHEA_NUTS: URIRef  # Refers to the presence of Shea nuts [Vitellaria paradoxa C.F. Gaertn. (Sapotaceae)] and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SHELLFISH: URIRef  # Refers to the presence of shellfish and its derivatives as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SHK: URIRef  # Refers to the presence of Shark and its derivates in the product. - Family/Genus/Species: (various) - Also known as: Atlantic Angel Shark, Basking Shark, Bigeye Thresher Shark, Bignose Shark, Black Dogfish, Blacknose Shark, Blacktip Reef Shark, Blacktip Shark, Blue Shark, Bonnethead, Brown Smoothhound, Bull Shark, Catshark, Common Thresher Shark, Dogfish Shark, Dusky Shark, Finetooth Shark, Gray Reef Shark, Great Hammerhead, Great White Shark, Grey Smoothhound, Hammerhead Shark, Large Spotted Dogfish, Lemon Shark, Leopard Shark, Lesser Spotted Dogfish, Longfin Mako Shark, Mako Shark, Narrowtoothed Shark, Night Shark, Northern Dogfish, Pacific Angel Shark, Pelagic Thresher Shark, Porbeagle, Reef Shark, Salmon Shark, Sandbar Shark, Scalloped Hammerhead, School Shark, Sevengill Shark, Shortfin Mako Shark, Silky Shark, Silvertip Shark, Sixgill Shark, Smalleye Hammerhead, Smalltail Shark, Smooth Dogfish, Smooth Hammerhead, Spinner Shark, Spiny Dogfish, Thresher Shark, Tiger Shark, White Shark, Whitetip Reef Shark, Whitetip Shark - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SHRIMP: URIRef  # Refers to the presence of Shrimp and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SI: URIRef  # Refers to the presence of hickory nuts and its derivatives in the product. - Family/Genus/Species: Carya. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SJ: URIRef  # Refers to the presence of Shea nuts and its derivatives in the product. - Family/Genus/Species: Vitellaria paradoxa. - Also known as: Shi nut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SK: URIRef  # Refers to the presence of Pili nuts and its derivatives in the product. - Family/Genus/Species: Canarium ovatum. - Also known as: Pili seeds. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SL: URIRef  # Refers to the presence of Lichee nuts and its derivatives in the product. - Family/Genus/Species: Litchi chinensis. - Also known as: Lichee seeds. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SM: URIRef  # Refers to the presence of Macadamia nuts and its derivatives in the product. - Family/Genus/Species: Macadamia. - Also known as: Queensland nut, Bush nut, Maroochi nut, Bauple nut and Hawaii nut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SMELT: URIRef  # Refers to the presence of Smelt and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SMF: URIRef  # Refers to the presence of Schoolmaster and its Derivatives in the product. - Family/Genus/Species: Lutjanidae/Lutjanus/apodus - Also known as: Schoolmaster, Schoolmaster snapper - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SMR: URIRef  # Refers to the presence of Salmon roe and its derivatives in the product, as listed in in the product. - Family/Genus/Species: Salmo - Also known as: Salmon caviar, red caviar, or ikura - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SMT: URIRef  # Refers to the presence of Smelt and its derivates in the product. - Family/Genus/Species: Osmeridae/(various) - Also known as: Arctic Smelt, Argetine Smelt, Austrailian Smelt, Ayu, Big-Scale Smelt, Cucumberfish, Deepsea Smelt, Delta Smelt, Eulachon, European Smelt, Freshwater Smelt, Great Silver Smelt, Herring Smelt, Jacksmelt, Lesser Silver Smelt, Longfin Smelt, New Zealand Smelt, Night Smelt, Rainbow Smelt, Seep-sea Smelt, Smelt, Surf Smelt, Topsmelt, Typical Smelt, Whitebait Smelt - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SN: URIRef  # Refers to the presence of chestnuts and its derivatives in the product. - Family/Genus/Species: Castanea. - Also known as: Sardian nut, Jupiter's nut, and Spanish chestnut. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SNAPPER: URIRef  # Refers to the presence of Snapper and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SO: URIRef  # Refers to the presence of coconuts and its derivatives in the product. - Family/Genus/Species: Cocos nucifera. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SOLE: URIRef  # Refers to the presence of Sole and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SOYBEANS: URIRef  # Refers to the presence of soybeans and their derivatives in the product, as listed in as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_SP: URIRef  # Refers to the presence of Pecan nuts and its derivatives in the product. - Family/Genus/Species: Carya illinoinensis. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SPELT: URIRef  # Refers to the presence of spelt and spelt products (gluten containing grain) as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SPF: URIRef  # Refers to the presence of Scorpionfish and its Derivatives in the product. - Family/Genus/Species: Scorpaenidae/(various) - Also known as: California Scorpinfish, Dragonfish, False Jacopever, Firefish, Hunchback Scorpionfish, Large-headed Scorpionfish, Lionfish, Orange Scorpionfish, Plumed Scorpionfish, Stingfish, Turkeyfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SQU: URIRef  # Refers to the presence of Squid (Calamari) and its derivates in the product. - Family/Genus/Species: (various) - Also known as: Angola Flying Squid, Argentine Shortfin Squid, Armhook Squid , Arrow Squid, Atlantic Brief Squid, Beka Squid, Bigeye Squid, Bigfin Reef Squid, Bigfin Squid , Bobtail Squid , Bottletail Squid , Bush-club Squid, Calamari, California Market Squid, Cape Horn Squid, Caribbean Reef Squid, Cock-eyed Squid , Cuttlefish , Dwarf Bobtail Squid, European Flying Squid, European Squid, Fire Squid , Firefly Squid , Flying Squid, Giant Squid , Glacial Squid , Glass Squid, Grimaldi scaled Squid , Hooked Squid , Indian Squid, Japanese Flying Squid, Joubin's Squid , Jumbo Squid, Longfin Inshore Squid, Magistrate Armhook Squid, Midsize Squid, Mitre Squid, Neritic Squid, Northern Shortfin Squid, Octopus Squid , Panama Brief Squid, Patagonian Inshore Squid, Purpleback Flying Squid, Pygmy Squid , Pyjama Squid , Ram's horn Squid , Sharpear enope Squid , Southern Reef Squid, Southern Shortfin Squid, Stout Bobtail Squid, Wellington Flying Squid, Whip-lash Squid - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SQUID__28CALAMARI_29: URIRef  # Refers to the presence of Squid (Calamari) and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SR: URIRef  # Refers to the presence of brazil nuts and its derivatives in the product. - Family/Genus/Species: Bertholletia excelsa. - Also known as: Castanha. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SS: URIRef  # Refers to the presence of Sunflower seeds or its derivatives in the product in the product. - Family/Genus/Species: Helianthus - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_ST: URIRef  # Refers to the presence of Pistachio and its derivatives in the product. - Family/Genus/Species: Pistacia. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_STG: URIRef  # Refers to the presence of Sturgeon and its derivates in the product. - Family/Genus/Species: Acipenseridae/(various) - Also known as: Adriatic Sturgeon, Alabama Sturgeon, Amu Darya Sturgeon, Amur Sturgeon, Atlantic Sturgeon, Baikal Sturgeon, Beluga, Beluga Sturgeon, Bester, Chinese Sturgeon, Dwarf Sturgeon, European sea Sturgeon, Fringebarbel Sturgeon, Green Sturgeon, Gulf Sturgeon, Japanese Sturgeon, Kaluga Sturgeon, Lake Sturgeon, Pallid Sturgeon, Persian Sturgeon, Russian Sturgeon, Sakhalin Sturgeon, Shortnose Sturgeon, Shovelnose Sturgeon, Siberian Sturgeon, Starry Sturgeon, Stellate Sturgeon, Sterlet, Syr Darya Sturgeon, Thorn Sturgeon, White Sturgeon, Yangtze Sturgeon - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_STURGEON: URIRef  # Refers to the presence of Sturgeon and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SU: URIRef  # Refers to the presence of Salicylate and its derivatives in the product. - Family/Genus/Species: - Also known as: Salicylic acid. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SULPHUR_DIOXIDE: URIRef  # Refers to the presence of sulphur dioxide and sulphites as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SUNFLOWER_SEEDS: URIRef  # Refers to the presence of Sunflower Seeds or their derivatives in the product as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SW: URIRef  # Refers to the presence of Walnuts and its derivatives in the product. - Family/Genus/Species: Juglans. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_SWORDFISH: URIRef  # Refers to the presence of Swordfish and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_SX: URIRef  # Refers to the presence of pulses in the product. This excludes green beans and green peas, which are considered vegetable crops. Also excluded are crops that are mainly grown for oil extraction. - Family/Genus/Species: Fabaceae. - Also known as: Dry seed legume Crops. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TA: URIRef  # Refers to the presence of 3-Aminophenol in the product. - CAS Registry Number: 591-27-5 - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TD: URIRef  # Refers to the presence of Toluene-2,5-diamine in the product. - CAS Registry Number: 95-70-5 - Also known as: Toluene-2,5-diamine - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TFD: URIRef  # Refers to the presence of Tilefish and its Derivatives in the product. - Family/Genus/Species: Malacanthidae/(various) - Also known as: Blue Tilefish, Blueline Tilefish, Golden Tilefish, Goldface Tilefish, Ocean Whitefish, Pacific Golden-eyed Tilefish, Pacific Sandperch, Sand Tilefish, Tilefish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TILAPIA: URIRef  # Refers to the presence of Tilapia and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_TOLUENE_2_2C5_DIAMINE: URIRef  # Refers to the presence of Toluene-2,5-diamine as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_TR: URIRef  # Refers to the presence of Triticale and its derivatives in the product. - Family/Genus/Species: × Triticosecale. - Also known as: Ryewheat. - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TREE_NUTS: URIRef  # Refers to the presence of tree nuts and their derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName. Tree nuts can include almonds, hazelnut, walnut, cashews, etc.
    AllergenTypeCode_TREE_NUT_TRACES: URIRef  # Contains Traces of Tree Nuts, i.e. almonds, various kinds of tree nuts.
    AllergenTypeCode_TRITICALE: URIRef  # Refers to the presence of Triticale and their derivatives as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_TROUT: URIRef  # Refers to the presence of Trout and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_TTD: URIRef  # Refers to the presence of Tomato and its derivatives in the product. - Family/Genus/Species: Solanum lycopersicum. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TUNA: URIRef  # Refers to the presence of Tuna and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_TUR: URIRef  # Refers to the presence of Turbot and its derivates in the product. - Family/Genus/Species: Scophthalmidae/Scophthalmus/S. maximus - Also known as: Brat, Breet, Britt, Butt, Diamond Turbot, Greenland Turbot, Hornyhead Turbot, New Zealand Turbot, Spottail Spiny Turbot, Spotted Turbot, Spring Turbot, Turbot - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_TURBOT: URIRef  # Refers to the presence of Turbot and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_UM: URIRef  # Refers to the presence of molluscs and its derivates in the product. - Family/Genus/Species: Mollusca (various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_UN: URIRef  # Refers to the presence of Shellfish in the product. Shellfish is a colloquial and fisheries term for exoskeleton-bearing aquatic invertebrates used as food, including various species of molluscs, crustaceans, and echinoderms. - Family/Genus/Species: (various) - Also known as: (various) - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_UW: URIRef  # Refers to the presence of Wheat and its derivatives in the product. - Family/Genus/Species: Triticum. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_WALLEYE: URIRef  # Refers to the presence of Walleye and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_WALNUTS: URIRef  # Refers to the presence of walnut and walnut products as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_WFD: URIRef  # Refers to the presence of Wolffish and its Derivatives in the product. - Family/Genus/Species: Anarhichadidae/Anarhichas or Anarrhichthys/(various) - Also known as: Atlantic Wolffish, Bering Wolffish, Northern Wolffish, Sea wolves, Spotted Wolffish, Wolffish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_WHEAT: URIRef  # Refers to the presence of wheat and their derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName
    AllergenTypeCode_WHELKS: URIRef  # Refers to the presence of Whelks and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_WHITEFISH: URIRef  # Refers to the presence of Whitefish and their derivatives in the product, as listed as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_WHITING: URIRef  # Refers to the presence of Whiting and its derivatives in the product, as listed in the regulations specified in AllergenSpecificationAgency and AllergenSpecificationName.
    AllergenTypeCode_WHK: URIRef  # Refers to the presence of Whelks and its derivates in the product. - Family/Genus/Species: Buccinidae or Ranellidae or Trochidae/(various) - Also known as: Busycon Whelk, Channeled Whelk, Common Periwinkle, Dog Whelk, Maculated Ivory Whelk, Magpie Whelk, Pear Whelk, Scungili, Veined Rapa Whelk, West Indian Top Shell Whelk, Whelk, Wilk - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_WHT: URIRef  # Refers to the presence of Whiting and its derivates in the product. - Family/Genus/Species: Gadidae or Sciaenidae or Sillaginidae/(various) - Also known as: Argentine Hake, Blue Whiting, Cape Hake, Carolina Whiting, Chilean Hake, Deep-water Cape Hake, European Hake, European Whiting, Flat Head Sillago, Hoki, Japanese sillago, Japanese Whiting, King George Whiting, King Whiting, Northern Whiting, Pacific Whiting, Sand Whiting, School Whiting, Sea Mullet, Silver Hake, Silver Sillago, Southern Blue Whiting, Southern Hake, Southern Kingcroaker, Southern Kingfish - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_X99: URIRef  # Does not contain declaration obligatory allergens in the product. - Also known as: - Disclaimer: Refers to the absence of allergens in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    AllergenTypeCode_YMD: URIRef  # Refers to the presence of Yam and its derivatives in the product. - Family/Genus/Species: Dioscorea. - Also known as: - Disclaimer: Refers to the presence of the allergen in the product, as listed in the regulations specified by an agency and specification or any local market regulations.
    Altitude: URIRef  # The height above the surface of a defined geoid, typically the World Geodetic System (WGS 84) geoid for measurements from location sensors using satellite technology (e.g. GPS, Glonass, Galileo) , which approximates to the surface of the earth at sea level.  Positive values indicate height above the geoid surface. Negative values indicate depth below the geoid surface.  SI Units: metres
    AmountOfSubstance: URIRef  # The amount of substance that contains a number of atoms, molecules etc. that is equal to the Avogadro constant.  SI Units: mole
    AmountOfSubstancePerUnitVolume: URIRef  # The concentration of a solution expressed as the number of moles of dissolved substance per unit volume of solution.  SI Units: mole per cubic metre
    AnatomicalFormCode: URIRef
    AnatomicalFormCode_BELLY: URIRef
    AnatomicalFormCode_BLOOD: URIRef
    AnatomicalFormCode_BONE: URIRef
    AnatomicalFormCode_BRAIN: URIRef
    AnatomicalFormCode_CARCASS_NONPOULTRY: URIRef
    AnatomicalFormCode_DIAPHRAM: URIRef
    AnatomicalFormCode_ESOPHAGUS: URIRef
    AnatomicalFormCode_FAT: URIRef
    AnatomicalFormCode_FEET: URIRef
    AnatomicalFormCode_FOREQUARTER: URIRef
    AnatomicalFormCode_GIZZARD: URIRef
    AnatomicalFormCode_HEAD: URIRef
    AnatomicalFormCode_HEADMEAT_CHEEKMEAT: URIRef
    AnatomicalFormCode_HEART: URIRef
    AnatomicalFormCode_HINDQUARTER: URIRef
    AnatomicalFormCode_HORN: URIRef
    AnatomicalFormCode_INTESTINE_LARGE: URIRef
    AnatomicalFormCode_INTESTINE_SMALL: URIRef
    AnatomicalFormCode_KIDNEY: URIRef
    AnatomicalFormCode_LIPS: URIRef
    AnatomicalFormCode_LIVER: URIRef
    AnatomicalFormCode_LUNGS: URIRef
    AnatomicalFormCode_MIXED_OFFAL: URIRef
    AnatomicalFormCode_MIXED_PARTS_FOR_GROUNDING_MINCING: URIRef
    AnatomicalFormCode_NECK: URIRef
    AnatomicalFormCode_PANCREAS: URIRef
    AnatomicalFormCode_SKIN: URIRef
    AnatomicalFormCode_STOMACH: URIRef
    AnatomicalFormCode_TAIL: URIRef
    AnatomicalFormCode_TENDONS: URIRef
    AnatomicalFormCode_TESTICLES: URIRef
    AnatomicalFormCode_THYMUS: URIRef
    AnatomicalFormCode_TONGUE: URIRef
    AnatomicalFormCode_TRIPE: URIRef
    AnatomicalFormCode_UNCLASSIFIED: URIRef
    AnatomicalFormCode_UNIDENTIFIED: URIRef
    AnatomicalFormCode_WHOLE_BIRD: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_NONPOULTRY_MEATPART_PIECE: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_POULTRY_PART: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_PRIMAL: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_RIBCUT: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_ROASTCUT: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_SLICE_CHOPCUT: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_SLICE_CUTLET: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_STEAK_CHOPCUT: URIRef
    AnatomicalFormCode_WHOLE_MUSCLE_SUBPRIMAL: URIRef
    Angle: URIRef  # The inclination of one line or plane to another.  Units: degrees, radians, etc.
    AngularAcceleration: URIRef  # The rate of change of angular velocity with respect to time.  SI Units: radian per second per second
    AngularMomentum: URIRef  # The integral over time of the torque acting on a body that is free to rotate, resulting in a corresponding change in its angular momentum.  SI Units: newton metre second, kilogram metre squared per second
    AngularVelocity: URIRef  # The rate of change of angle with respect to time; a measure of the number of revolutions per unit time.  SI Units: radian per second
    Area: URIRef  # The amount of two-dimensional space occupied, measured in units of length squared.  SI Units: square metre
    AuthenticityDetails: URIRef  # A set of details about covert or overt security features that may contribute to checking the authenticity of a product or product instance.
    AwardPrizeDetails: (
        URIRef  # Describes a prize or award won by a product or organization.
    )
    Beverage: URIRef  # Any potable liquid.
    Brand: URIRef  # Information on brands and sub-brands for a product.
    Capacitance: URIRef  # The capacitance of an isolated conductor is defined as the ratio of the total charge on it to its electric potential.  SI Units: farad
    CertificationDetails: URIRef  # Certification issued by a certifying body to a certification subject (Organization, Place, Product).
    CertificationStatus: (
        URIRef  # A set of codes for the status of a certification instance
    )
    CertificationStatus_ACTIVE: URIRef  # This certification instance is declared to be in effect for the certified subject.
    CertificationStatus_INACTIVE: (
        URIRef  # This certification instance is declared to be no longer in effect.
    )
    CheeseFirmnessCode: URIRef
    CheeseFirmnessCode_EXTRA_HARD: URIRef
    CheeseFirmnessCode_FIRM_SEMIHARD: URIRef
    CheeseFirmnessCode_HARD: URIRef
    CheeseFirmnessCode_SOFT: URIRef
    CheeseFirmnessCode_UNIDENTIFIED: URIRef
    Clothing: URIRef  # A product that is worn on the body.
    ColourCodeDetails: URIRef  # A set of colour code details (colour code, party controlling the code list) for the product.
    ColourCodeList_BUYER: URIRef  # Assigned by buyer.
    ColourCodeList_IFPS: URIRef  # International Federation for Produce Standards.
    ColourCodeList_NCS: URIRef  # Natural Colour System.
    ColourCodeList_NRF: URIRef  # National Retail Federation.
    ColourCodeList_PANTONE_HEXACHROME: URIRef  # Pantone Hexachrome.
    ColourCodeList_PANTONE_MATCHING: URIRef  # Pantone Matching System.
    ColourCodeList_PANTONE_PROCESS_COLOUR: URIRef  # Pantone Process Colour System.
    ColourCodeList_PANTONE_TEXTILE: (
        URIRef  # Pantone Textile. Same as GS1 ColourCodeList Code 5
    )
    ColourCodeList_RAL: URIRef  # Farbsystem RAL Colour System.
    ColourCodeList_SELLER: URIRef  # Assigned by seller.
    ColourCodeList_WWS: URIRef  # Waren Wirtschafts System.
    ColourCodeListCode: URIRef
    Conductance: URIRef  # The ratio of the current in the conductor to the potential difference between its ends; reciprocal of resistance.  SI Units: siemen
    Conductivity: URIRef  # A measure of how strongly a material conducts electric current. The ratio of the current density to the electric field that causes the current to flow.  SI Units: siemen per metre
    ConsumerLifestageCode: URIRef
    ConsumerLifestageCode_ADULT: URIRef
    ConsumerLifestageCode_ALL_AGES: URIRef
    ConsumerLifestageCode_BABY_INFANT: URIRef
    ConsumerLifestageCode_CHILD_1_To_2_YEARS: URIRef
    ConsumerLifestageCode_CHILD_2_YEARS_ONWARDS: URIRef
    ConsumerLifestageCode_UNCLASSIFIED: URIRef
    ConsumerLifestageCode_UNIDENTIFIED: URIRef
    ConsumerSalesConditionsCode: URIRef
    ConsumerSalesConditionsCode_BTC: URIRef  # Products that are sold without a prescription but must be distributed through a pharmacy.
    ConsumerSalesConditionsCode_OTC: URIRef  # Products that may be sold without a prescription. These products are generally available without restrictions.
    ConsumerSalesConditionsCode_PRESCRIPTION_REQUIRED: URIRef  # Product may only be sold or dispensed under the direction of a prescription.
    ConsumerSalesConditionsCode_RESTRICTED_TO_SELL_16: URIRef  # Based upon legal regulatory restrictions it is illegal to sell the product to anyone under the age of 16 years old.
    ConsumerSalesConditionsCode_RESTRICTED_TO_SELL_18: URIRef  # Based upon legal regulatory restrictions it is illegal to sell the product to anyone under the age of 18 years old.
    ConsumerSalesConditionsCode_RESTRICTED_TO_SELL_21: URIRef  # Based upon legal regulatory restrictions it is illegal to sell the product to anyone under the age of 21 years old.
    ContactPoint: URIRef  # Information on an individual or department acting as point of contact for an organiation.
    Count: URIRef  # A measure of the total quantity of something; the number of individual units present.  Typically dimensionless (no units)
    Country: URIRef  # Country is a complex data type that indicates a country and a country subdivision.
    Density: URIRef  # The mass per unit volume of a substance.  SI Units: kilogram per cubic metre
    DietTypeCode: URIRef
    DietTypeCode_COELIAC: URIRef  # Denotes a product that can be safely consumed by a person with coeliac disease. Coeliac disease is caused by a reaction to gladin (a gluten protein found in wheat) and similar proteins found in other crops.
    DietTypeCode_DIETETIC: URIRef  # Denotes a product that is specially prepared or processed for people on restrictive diets.
    DietTypeCode_FREE_FROM_GLUTEN: URIRef  # Denotes a product that can be used in a gluten free diet, as specified by the appropriate authority within a target market.
    DietTypeCode_HALAL: URIRef  # Denotes selling or serving food ritually fit according to Islamic dietary laws.
    DietTypeCode_KOSHER: URIRef  # Denotes selling or serving food ritually fit according to Jewish dietary laws.
    DietTypeCode_ORGANIC: URIRef  # Denotes a food product that was produced with the use of feed or fertiliser of plant or animal origin, without employment of chemically formulated fertilisers, growth stimulants, antibiotics or pesticides.
    DietTypeCode_VEGAN: URIRef  # Denotes a food product which contains no animal food or dairy products.
    DietTypeCode_VEGETARIAN: URIRef  # Denotes a product that contains no meat, fish or other animal products.
    DietTypeCode_WITHOUT_BEEF: URIRef  # Denotes a product that contains no beef or beef-products. Beef is considered to be a taboo food product by some religions most notable Hinduism, Buddhism and Jainism.
    DietTypeCode_WITHOUT_PORK: URIRef  # Denotes a product that contains no pork meat.
    DietTypeCodeDetails: URIRef  # A set of diet type code details (diet type code and diet type sub code) for the product.
    Dimensionless: URIRef  # A measurement whose units are dimensionless.  gs1:Count or gs1:VolumeFraction or gs1:RelativeHumidity should be used in preference if appropriate.
    Discount: URIRef  # Provides information on a discount applicable to an offer for example 2 percent.
    DiscountTypeCode: URIRef
    DiscountTypeCode_BOGO: URIRef  # Buy one item and get the second item free of charge
    DiscountTypeCode_DISCOUNTED_ITEM: (
        URIRef  # A discount on the item expressed as an amount (value and currency)
    )
    DiscountTypeCode_FREE_GIFT: URIRef  # A gift given to a consumer as part of a promotional contingent on the consumer making a purchase of another item or items.
    DiscountTypeCode_FREE_SHIPPING: URIRef  # No charge for shipping.
    DiscountTypeCode_OTHER: URIRef  # A discount other than the ones on this list.
    DiscountTypeCode_PERCENTAGE_OFF: URIRef  # A percentage off the product price.
    DoseEquivalent: URIRef  # The product of the absorbed dose multiplied by a Q factor (relating to the type of radiation) and a factor relating to all relevant aspects of the body being irradiated, multiplied by the exposure time.  SI Units: sievert
    DoseEquivalentRate: URIRef  # The product of the absorbed dose rate multiplied by a Q factor (relating to the type of radiation) and a factor relating to all relevant aspects of the body being irradiated.  SI Units: sievert per second
    DynamicViscosity: URIRef  # The value of the tangential force per unit area which is necessary to maintain unit relative velocty between two parallel planes unit distance apart in a fluid.  SI Units: pascal
    ERROR_CONDITION: URIRef  # Indicates the reporting of an error condition detected by a sensor device
    ElectricCharge: URIRef  # Quantity of unbalanced electricity in an object, i.e. excess or deficiency of electrons, resulting in negative or positive electrification, respectively.  SI Units: coulomb
    ElectricCurrent: URIRef  # Rate of flow of charge in a substance, whether solid, liquid or gas.  SI Units: ampere
    ElectricCurrentDensity: URIRef  # Rate of flow of charge in a substance per unit area perpendicular to the current.  SI Units: ampere per square metre
    ElectricFieldStrength: URIRef  # The electric force acting on a unit charge. The linear gradient of the electrostatic potential.  SI Units: volt per metre = newton / coulomb
    Energy: URIRef  # A measure of a the capacity of a system or body to do work.  SI Units: joule
    Exposure: URIRef  # The product of light intensity and time duration of the exposure.  SI Units: lux second
    FoodAndBeveragePreparationInformation: URIRef  # Food and Beverage Preparation Information is a complex data type that indicates a preparation state code and preparation instructions.
    FoodBeverageRefrigerationClaimCode: URIRef
    FoodBeverageRefrigerationClaimCode_CAN_BE_REFRIGERATED: URIRef
    FoodBeverageRefrigerationClaimCode_MUST_BE_REFRIGERATED: URIRef
    FoodBeverageRefrigerationClaimCode_SHELF_STABLE: URIRef
    FoodBeverageRefrigerationClaimCode_UNIDENTIFIED: URIRef
    FoodBeverageTargetUseCode: URIRef
    FoodBeverageTargetUseCode_ANY_MEAL: URIRef
    FoodBeverageTargetUseCode_BREAKFAST: URIRef
    FoodBeverageTargetUseCode_MAIN_MEAL: URIRef
    FoodBeverageTargetUseCode_PORTABLE_MEAL: URIRef
    FoodBeverageTargetUseCode_SNACK: URIRef
    FoodBeverageTargetUseCode_UNCLASSIFIED: URIRef
    FoodBeverageTobaccoIngredientDetails: URIRef  # Food Beverage Tobacco Ingredient is a complex data type that includes an ingredient statement and details.
    FoodBeverageTobaccoProduct: URIRef  # A food, beverage or tobacco product.
    Footwear: URIRef  # Outerwear that is worn on the feet such as shoes or boots.
    FootwearFasteningTypeCode: URIRef
    FootwearFasteningTypeCode_MULTIPLE_FASTENING: URIRef
    FootwearFasteningTypeCode_SHOE_LACE: URIRef
    FootwearFasteningTypeCode_SLIP_ON_WITHOUT_ELASTIC: URIRef
    FootwearFasteningTypeCode_SLIP_ON_WITH_ELASTIC: URIRef
    FootwearFasteningTypeCode_STRAP: URIRef
    FootwearFasteningTypeCode_UNCLASSIFIED: URIRef
    FootwearFasteningTypeCode_UNIDENTIFIED: URIRef
    FootwearFasteningTypeCode_VELCRO: URIRef
    Force: URIRef  # The rate of change of linear momentum of a body on which a force acts. A force acting on a body which is free to move produces an acceleration in the motion of the body.  SI Units: newton
    Frequency: URIRef  # The rate of repetition of a periodic oscillation or disturbance; the number of cycles per unit time.  SI Units: hertz
    FreshOrSeawaterFarmedCode: URIRef
    FreshOrSeawaterFarmedCode_FRESHWATER_FARMED: URIRef
    FreshOrSeawaterFarmedCode_SEAWATER_FARMED: URIRef
    FreshOrSeawaterFarmedCode_UNCLASSIFIED: URIRef
    FreshOrSeawaterFarmedCode_UNIDENTIFIED: URIRef
    FruitsVegetables: URIRef  # Contains properties related specifically to fruit and vegetable products.
    GLN_TypeCode: URIRef  # GLN Type Code indicates what type of thing is being identified by a GLN. gs1:GLN_TypeCode value selections SHALL NOT contain both gs1:GLN_TypeCode-FIXED_PHYSICAL_LOCATION and gs1:GLN_TypeCode-MOBILE_PHYSICAL_LOCATION.
    GLN_TypeCode_DIGITAL_LOCATION: URIRef  # An electronic (non-physical) address that is used for communication between computer systems.
    GLN_TypeCode_FIXED_PHYSICAL_LOCATION: URIRef  # Fixed physical location - a tangible place that does not change locations and may be represented by an address, coordinates, or other means.
    GLN_TypeCode_FUNCTION: URIRef  # An organisational subdivision or department.
    GLN_TypeCode_LEGAL_ENTITY: URIRef  # Any business, government body, department, charity, individual, or institution that has standing in the eyes of the law and has the capacity to enter into agreements or contracts.
    GLN_TypeCode_MOBILE_PHYSICAL_LOCATION: URIRef  # Mobile physical location - a tangible place that is expected to change locations and may be represented by an address, coordinates, or other means.
    GeoCoordinates: URIRef  # The geographic coordinates of a place or event.
    GeoShape: URIRef  # The geographic shape of a place. A GeoShape can be described using several properties whose values are based on latitude/longitude pairs. Either whitespace or commas can be used to separate latitude and longitude; whitespace should be used when writing a list of several such points.
    GrowingMethodCode: URIRef
    GrowingMethodCode_CAGE_FREE: URIRef  # Animal is not confined to a cage.
    GrowingMethodCode_CLONED_FOODS: (
        URIRef  # Product is a result of genetic engineering.
    )
    GrowingMethodCode_CONVENTIONAL: URIRef  # Foods grown non-organically, either indoors or outdoors without any special processes.
    GrowingMethodCode_FARM_RAISED: URIRef  # Animal is raised on a farm.
    GrowingMethodCode_FIELD_GROWN: URIRef  # Plants Grown Outdoors
    GrowingMethodCode_FLY_FREE: URIRef  # Citrus Grown in an area certified to be free of all Caribbean Fruit Flies based on trappings
    GrowingMethodCode_FREE_RANGE: URIRef  # A method that animals are allowed to roam with little restriction to their movements.
    GrowingMethodCode_GRASS_FED: URIRef  # Animal is predominately fed grass or forage.
    GrowingMethodCode_GREENHOUSE: (
        URIRef  # Plants that are grown and cultivated in an indoor covered place.
    )
    GrowingMethodCode_HUMANELY_RAISED: URIRef  # A process where animals are raised such that the welfare of the animal is a foremost concern.
    GrowingMethodCode_HYDROPONIC: (
        URIRef  # Plants grown using mineral nutrient solutions instead of soil.
    )
    GrowingMethodCode_INTEGRATED_PEST_MANAGEMENT: URIRef  # (IPM) Plants grown using a pest control strategy that uses an array of complimentary methods: mechanical devices, physical devices, genetic, biological, legal, cultural management and chemical management. These methods are done in three stages: prevention, observation, and intervention. It is an ecological approach with a main goal of significantly reducing or eliminating the use of pesticides.
    GrowingMethodCode_ORGANIC: (
        URIRef  # Foods grown organically, either indoors or outdoors.
    )
    GrowingMethodCode_SHADE_GROWN: (
        URIRef  # Produce which has been grown under shade or grown under cloth.
    )
    GrowingMethodCode_SUSTAINABLE: URIRef
    GrowingMethodCode_WILD: URIRef  # The animal or plant was not inhibited or prohibited from roving, wandering, and not tamed or domesticated.
    Illuminance: URIRef  # The energy in the form of visible radiation reaching a surface per unit area in unit time; the amount of luminous flux per unit area.  SI Units: lux = 1 lumen per square metre
    Inductance: URIRef  # The magnitude of the property of an element or circuit to form a magnetic field and store magnetic energy when carrying a current. The property of an electric circuit or component that causes an electromotive force to be generated in it as a result of a change in the current flowing through the circuit (self inductance) or of a change in the current flowing through a neighbouring circuit with which it is magnetically linked (mutual inductance).  SI Units: henry
    Irradiance: URIRef  # The flux of radiant energy per unit area, especially an area perpendicular to the direction of travel through a medium. A measure of the radiant power per unit area that flows across a surface.  SI Units: watt per square metre
    KinematicViscosity: URIRef  # The ratio of the viscosity of a liquid to its density.  SI Units: square metres per second
    Length: URIRef  # The linear magnitude of any thing, as measured end to end.  Length, width, depth, height, diameter are all measured in units of length.  SI Units: metre
    LevelOfContainmentCode: URIRef
    LevelOfContainmentCode_CONTAINS: URIRef  # Intentionally included in the product.
    LevelOfContainmentCode_FREE_FROM: (
        URIRef  # The product is free from the indicated substance.
    )
    LevelOfContainmentCode_MAY_CONTAIN: URIRef  # The substance is not intentionally included, but due to shared production facilities or other reasons, the product may contain the substance.
    LinearMomentum: URIRef  # The impulse is the integral over time of the force acting between two colliding bodies. Linear momentum of a body is the product of its mass and its velocity.  SI Units: newton seconds
    LocationID_Details: URIRef  # Government bodies, trade organisations, and other parties issue identifiers that are associated to locations. Linking these identifiers to GLN and one another supports consolidating records, mapping related, collaborative identifiers, enhances search ability and enables more efficient transitions between identifiers.  This class provides a mechanism for connecting and sharing location identifiers.
    LocationID_Type: URIRef
    LocationID_Type_BIC_FACILITY: URIRef  # The BIC Facility Code (BFC) began life in the 1980s as the 'LoCode' identifier under ISO 9897. Now a 'child code' of the UN/Locode, the BIC Facility Code is used to identify container facilities such as depots, container yards, container freight stations, M&R vendors and other facilities in the container supply chain. The BIC Facility Code is complementary to the SMDG Ocean Terminal Code, which is also a child code of the UN/Locode. The BIC Facility Code covers container facility types other than ocean terminals.
    LocationID_Type_CRD_LOCATION_CODE: URIRef  # The Central Reference File Database (CRD) (formerly known as Central Repository Domain) is a centralised database that stores Location Codes and Company Codes required by European regulation, and makes them available to users. CRD contains the following reference files: - List of Countries (ISO 3166) - The Location Reference File which uniquely identifies physical rail points (e.g. stations, customer sidings, loading places) containing the Location Code (which includes the Country Code) - The Partner Reference File uniquely identifies all rail actors who exchange information (Company Codes); Each company actor must have a unique Company Code assigned by UIC
    LocationID_Type_ENI_NUMBER: URIRef  # An ENI number (European Number of Identification or European Vessel Identification Number) is a registration for ships capable of navigating on inland European waters. It is a unique, eight-digit identifier that is attached to a hull for its entire lifetime, independent of the vessel's current name or flag. ENI was introduced by the Inland Transport Committee of the United Nations Economic Commission for Europe in their meeting on 11-13 October 2006 in Geneva. It is based on the Rhine Vessel certification system previously used for ships navigating the Rhine, and is comparable to the IMO ship identification number.
    LocationID_Type_FR_SIRET: URIRef  # The SIRET number, issued by Insee (the National Institute of Statistics and Economic Studies) identifies each establishment that is part of a company in France. There are as many SIRET numbers as there are establishments in the company. An establishment is a geographically located operating or production unit, separated but legally dependent on a company. It is the place where the company's activity is carried out. It is composed of 14 digits: the 9 digits of the SIREN number + the 5 digits of the NIC (internal classification number specific to each establishment).
    LocationID_Type_IATA_CODE: URIRef  # Three-letter geocode designating many airports and metropolitan areas around the world, defined by the International Air Transport Association (IATA). The IATA three-letter codes are a subset of the UN/LOCODE codelist.
    LocationID_Type_IMO_NUMBER: URIRef  # IMO number is an important identifier given to oil/gas vessels, shipping vessels, and fishing vessels that is painted visibly across the vessel and bolted to the hull
    LocationID_Type_ISPS_CODE: URIRef  # The International Ship and Port Facility Security Code (ISPS Code) is an International code that was conceived following the September 11th 2001 terrorists attacks in the USA.  Its primary purpose is to identify and counter any terrorist threat to the Maritime Industry particularly against ships and ports. The code also serves to improve security against armed robbery, theft and piracy. The code came into force in 2004 and prescribes responsibilities to: 1) Governments 2) Shipping companies 3) Shipboard personnel 4) Port/facility personnel
    LocationID_Type_ISRS_LOCATION_CODE: URIRef  # The International Ship Reporting Standard (ISRS) location code is a 20 character alphanumeric code consisting of: - UN country code (2 characters) e.g., NL = Netherlands, - UN location code (3 characters) e.g., RTM = Rotterdam, - Fairway section code (5 characters) e.g., 00102 = Nieuwe Maas, - Object reference code (5 characters) e.g., 66666 = ID administration or terminal code, - Fairway section hectometre e.g., 00050 = hectometres from zero point of Fairway section 00102.  The ISRS Location Code is created once and shall not be changed throughout the lifetime of the object. The Standard / Commission Regulation for Electronic Ship Reporting requires the ISRS Location Code of all objects relevant for reporting of voyages, e.g. ports, terminals, passage points, etc.
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_1: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_10: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_2: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_3: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_4: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_5: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_6: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_7: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_8: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_LOCATION_FOR_INTERNAL_USE_9: (
        URIRef  # Identification used for internal mapping purposes.
    )
    LocationID_Type_MMSI_NUMBER: URIRef  # Maritime Mobile Service Identities (MMSIs) are nine-digit numbers used by maritime digital selective calling (DSC), automatic identification systems (AIS), and certain other equipment to uniquely identify a ship or a coast radio station.
    LocationID_Type_OAR_ID: URIRef  # Open Apparel Registry ID. A sixteen-digit numbering system which uniquely identities global apparel facilities. The ID consists of a Country code, Origin date (the date the facility first appeared in the registry), a General ID and Check ID. OAR IDs are allocated by the Open Apparel Registry to all facilities contributed to the database for the purposes of enabling industry collaboration and improved identification of factories, as well as powering interoperability between industry databases.
    LocationID_Type_OPEN_LOCATION_CODE: URIRef  # The Open Location Code is a geocode system for identifying an area anywhere on the Earth. It was developed at Google's Zürich engineering office, and released late October 2014. Location codes created by the OLC system are referred to as 'plus codes'.
    LocationID_Type_SMDG_CODE: URIRef  # The SMDG Terminal Code List (TCL) contains codes for container handling terminal facilities that are called by seagoing cargo vessels in maritime transport.
    LocationID_Type_UN_LOCODE: URIRef  # UN/LOCODE, the United Nations Code for Trade and Transport Locations, is a geographic coding scheme developed and maintained by United Nations Economic Commission for Europe.
    LocationID_Type_US_CIF_CODE: URIRef  # The Customer Identification File (CIF) is an industry reference file (for the USA), managed by Railinc, that contains the name, physical mailing and billing address, corporate parent information and a unique 13-character identification code for each location and sub-location of a transportation-carrier customer. Railroads use the identification code to accurately identify customers and their locations, ensuring each party in the transaction is referencing the same physical customer location.
    LocationID_Type_US_EST_NUMBER: URIRef  # All containers of meat, poultry, and egg products must be labeled with a USDA mark of inspection and establishment (EST number), which is assigned to the plant where the product was produced.
    LocationID_Type_US_FEI: URIRef  # An FDA Establishment Identification (FEI) number is a unique identifier issued by FDA to track inspections of the regulated establishment or facility. FEI numbers are also used to track GDUFA facility fee payments.
    LocationID_Type_US_HIN_IDENTIFICATION: URIRef  # The HIN is a unique combination of letters and/or numbers permanently affixed to the vessel. All boats must be registered with the USCG (United States Coast Guard ) in order to track accidents and history of boats. Information about a boat's records may be found by using a vessel documentation search by Hull ID Number (HIN).
    LocationID_Type_US_MINE_ID: URIRef  # All mines are required to apply for an MSHA mine identification number. An MSHA ID is required for each mine site and must be issued before any operations may begin. A mine ID may be requested by completing the online form or by contacting U.S. district office.
    LocationID_Type_US_TCN_CODE: URIRef  # The Terminal Control Locations Directory lists all approved terminals registered as part of the taxable fuel bulk delivery system. Terminals are listed by the terminal number.
    LocationRoleType: URIRef  # Indicates the role and/or purpose of a location (i.e., fixed or mobile physical location or digital location) identified with a GLN.
    LocationRoleType_AGED_CARE_SERVICE: (
        URIRef  # Service or facility providing aged care.
    )
    LocationRoleType_AIRCRAFT: URIRef  # A vehicle or machine that is able to fly by gaining support from the air.
    LocationRoleType_AIRPORT: URIRef  # A location with airfield and terminal facilities for aircraft take-off and landing, serving as an air transport terminal at which aircraft may call to receive services such as loading and discharging passengers, crews or cargo, refuelling, restocking, repair etc.
    LocationRoleType_AIRPORT_GATE: URIRef  # Entrance to a movable passage like a tunnel or bridge leading to the aircraft
    LocationRoleType_AMBULANCE_SERVICE: (
        URIRef  # Provides initial patient care and transportation to a medical facility
    )
    LocationRoleType_AMUSEMENT_ENTERTAINMENT_GAMING: (
        URIRef  # Provides recreation and entertainment services
    )
    LocationRoleType_ASSEMBLY: URIRef  # An area where components are put together into an end product, appropriate to the process concerned.
    LocationRoleType_ATM: URIRef  # An automated teller machine (ATM) is an electronic banking outlet that allows customers to complete basic transactions without the aid of a branch representative or teller. ATMs are known in different parts of the world as automated bank machines (ABM) or cash machines.
    LocationRoleType_BACKROOM: URIRef  # An area within a store (all formats - club, etc.) used to hold product until it is purchased or can be moved to the sales floor.
    LocationRoleType_BANK: (
        URIRef  # A location offering financial services to consumers and/or businesses.
    )
    LocationRoleType_BERTH: URIRef  # A berth is a specialised space or part of a wharf space assigned to or taken up by a ship or vessel when anchored or stationary alongside a quay, wharf, jetty, or other structure. As a berth is usually a straight line segment between two points, a wharf may consist of several individual berths and represent a grouping of berths.
    LocationRoleType_BIRTH_AREA: URIRef  # The place the animal was born/hatched.  Note: the term animal includes but is not limited to mammals, birds, fish and crustaceans.
    LocationRoleType_BOAT: URIRef  # A watercraft of a large range of types and sizes, but generally smaller than a ship,
    LocationRoleType_BOTTLING_SITE: URIRef  # A location or area within a larger location where beverages are bottled.
    LocationRoleType_BOX_CRUSHER: URIRef  # A Baler used to compact recycled materials (e.g. corrugated boxes, slip sheets and packaging material).
    LocationRoleType_BRANCH_LOCATION: URIRef  # A location for an organization segment that operates in a different physical location or jurisdiction than its parent organization, although is considered as an extension of the parent organization (i.e., same legal entity.).
    LocationRoleType_CASH_CARRY_STORE: URIRef  # Location where goods are paid for in full at the time of purchase and taken away by the purchaser.
    LocationRoleType_CITY_CENTER_SHOP: URIRef  # The product is intended to be sold in a city center. A city center shop is centrally located in the commercial, cultural and often the historical, political and geographic heart of a city, especially those in the Western world.
    LocationRoleType_CLINIC: URIRef  # A location serving as a health facility, often associated with a hospital, care practitioner or medical school for example, that is primarily focused on the care of outpatients, where medical treatment or advice can be administered, especially of a specialist nature.
    LocationRoleType_CLINICAL_TRIAL_SITE: URIRef  # A location designated by a healthcare provider as a site where clinical trials are conducted. In many cases clinical trial sites are hospital facilities with specialised hospital pharmacies, or retail pharmacies on site, but may also include trial specific sites such as a clinical trial subject's residence.
    LocationRoleType_COLLECTION_CENTER: URIRef  # A location where purchased products may be collected by the purchaser or a delegated party.
    LocationRoleType_CONSOLIDATING_CENTER: URIRef  # A facility where smaller shipments or consignments are combined into larger consignments bound for a destination.
    LocationRoleType_CONSTRUCTION_SITE: URIRef  # A construction site is an area or piece of land on which construction works are being carried out.
    LocationRoleType_CONTAINER_DECK: (
        URIRef  # An area on board a shipping vessel where containers are loaded.
    )
    LocationRoleType_CONTROLLED_SUBSTANCE_AREA: URIRef  # A caged and locked area in which regulated, controlled substance pharmaceuticals are held while awaiting shipment.
    LocationRoleType_CONVENIENCE_STORE: URIRef  # A location for a type of small format retail store often located with or connected to a gas/fuel station. Convenience stores usually provide extended trading hours, operating earlier and later than traditional retail stores.
    LocationRoleType_CONVEYOR_BELT: URIRef  # A continuous moving strip or surface that is used for transporting single cartons or a load of objects from one place to another.
    LocationRoleType_CORRECTION_FACILITY: (
        URIRef  # Provides detention and rehabilitative services to inmates
    )
    LocationRoleType_CUSTOMER_PICK_UP_AREA: URIRef  # An area, usually within a store or collection center, that is reserved specifically for consumers to collect goods purchased online (sometimes known as 'click and collect'), or goods purchased in store to be collected at a later time or date (e.g., paid in instalments, bulky goods, goods requiring staff assistance etc). A customer pick-up area may also enable access by vehicle.
    LocationRoleType_CUSTOMS_BORDER_CONTROL: URIRef  # A location where cross-border procedures and formalities may be executed and fulfilled. Examples of these include passport control, importation of goods, sanitary and phytosanitary (SPS) formalities etc.
    LocationRoleType_DENTAL_HEALTH_SERVICE: (
        URIRef  # Provides oral health treatment and support services
    )
    LocationRoleType_DEPOT: URIRef  # A location where vehicles such as those used for transportation (e.g., trucks, trains) or services (e.g., mobile food truck, exhibition cart) can be housed, maintained and deployed from.
    LocationRoleType_DISPENSER: URIRef  # Tablet, caplet or capsule dispensing machine in which bulk product has been placed to be dispensed on a prescription basis.
    LocationRoleType_DISTRIBUTION_CENTER: URIRef  # A specialised warehouse space that serves as a hub for the strategic storage of goods, for the purpose of picking, packing and shipping to another location, or the final destination.
    LocationRoleType_DOCK: URIRef  # An area within a facility where transportation such as trucks or rail cars can be loaded with goods for dispatch (i.e., outbound shipping, or sending) or unloaded with goods delivered (i.e., inbound shipping or receiving). Sometimes known as a dock door, a loading or unloading dock or bay, these areas are also used to hold goods temporarily ahead of being stored, or loaded for delivery, so may also include controlled environments such as for cold storage. Docks are designated for use with inbound or outbound shipments, to enable transportation carriers to schedule their arrival for loading or unloading based on dock availability and other critical logistics details such as dock heights, storage conditions and type of equipment on hand. Dock use designations can change frequently based on facility capacity and day-to-day events.
    LocationRoleType_DOCTOR_OFFICE: URIRef  # A room or clinic where a doctor works.
    LocationRoleType_DRUG_STORE: URIRef  # Establishment that offers personal care goods, toiletries and non-controlled drugs which can be obtained without a prescription. Within the Netherlands this establishment is a different than a retail pharmacy (referred to in the code list as DRUG).
    LocationRoleType_DUTY_FREE_STORE: URIRef  # A location for a type of retail store that is exempt from the payment of certain local or national taxes and duties, on the requirement that the goods sold will be sold to travellers who will take them out of the country. Duty-free stores are usually located within an international travel facility such as an airport or passenger terminal for rail or ferry.
    LocationRoleType_EARLY_CHILDHOOD_EDUCATING_AND_CENTER: URIRef  # Premises used regularly for the education or care of children who are pre-school age or younger.
    LocationRoleType_EDI_STATION: (
        URIRef  # Digital location where the EDI messages can be sent and received from.
    )
    LocationRoleType_EDUCATION_FACILITY: URIRef  # A location used as a public or private education premise where primary, secondary or tertiary education is conducted.
    LocationRoleType_ELECTRONICS_AREA: URIRef  # A specific area within the store for holding electronic products such as TV's, DVD players, etc.
    LocationRoleType_EMERGENCY_DEPARTMENT_AREA: URIRef  # An area of a hospital especially equipped and staffed for emergency care.
    LocationRoleType_END_CAP_AREA: URIRef  # A specific internal location on the sales floor, typically at the end of an aisle, for displaying product.
    LocationRoleType_ENTRANCE_GATE: URIRef  # A location that is a type of opening to allow entry to an enclosed place such as a terminal, warehousing, healthcare facility, or agricultural facility or parts thereof for example. For a gate designated as an exit only, see EXIT_GATE. For a gate designated as both an entry and exit, see GATE.
    LocationRoleType_EXIT_GATE: URIRef  # A location that is a type of opening to allow exit from an enclosed place such as a terminal, warehousing, healthcare facility, or agricultural facility or parts thereof for example. For a gate designated as an entry only, see ENTRANCE_GATE. For a gate designated as both an entry and exit, see GATE.
    LocationRoleType_FARM: URIRef  # A location used for agricultural production purposes, such as for growing crops, rearing animals or both. A farm often serves as a hub for a variety of agricultural activities and typically consists of various structures or areas such as barns, silos, feed areas or fields for example.
    LocationRoleType_FEEDLOT_SITE: (
        URIRef  # A location or area within a larger location where livestock are fed.
    )
    LocationRoleType_FIELD: URIRef  # An area of open land, that may be used for agricultural purposes, such as for growing crops and/or rearing animals. A field may or may not be part of a farm, as it may also exist as a fenced but open space for pasture, devoid of infrastructure such as a wild meadow.
    LocationRoleType_FIXED_READER: URIRef  # A location equipped with any fixed read point configuration (reader and antennas) for the purpose of capturing data from an RFID device (e.g. read points at doorways or conveyors).
    LocationRoleType_FIXED_TRANSPORT_FACILITIES: URIRef  # A location with permanent facilities to load or discharge cargo, that does not fit within a maritime, rail, road, air, or multimodal type facility. For example, an oil platform or terminal.
    LocationRoleType_FOOD_BUSINESS: URIRef  # A location for businesses selling prepared food to consumers such as cafes, restaurants, food trucks.
    LocationRoleType_FREIGHT_HUB: URIRef  # A location that is an interchange point at which equipment or goods are exchanged between drivers and/or transport operators.
    LocationRoleType_FREIGHT_TERMINAL: URIRef  # An assigned area in which shipping containers of any type and size are prepared for loading into a transportation vehicle (e.g., truck, train, vessel or aeroplane) or where the containers are stacked immediately after unloading from a transportation vehicle.
    LocationRoleType_GARDEN_CENTER: (
        URIRef  # An establishment where plants and gardening equipment are sold.
    )
    LocationRoleType_GATE: URIRef  # A location that is a type of opening to allow both entry to and exit  from an enclosed place such as a terminal, warehousing, healthcare facility, or agricultural facility or parts thereof, for example. For a gate designated as an entry only, see ENTRANCE_GATE. For a gate designated as an exit only, see EXIT_GATE.
    LocationRoleType_GENERAL_MDSE_AREA: URIRef  # An area where typically - non-food products other than perishable, dry groceries and health and beauty care products that are displayed in stores on standard shelving. Examples include household cleaning products, paper napkins, laundry detergents, and insect repellents
    LocationRoleType_GOVERNMENT_DEPARTMENT_AGENCY: (
        URIRef  # Location where a government body conducts operations.
    )
    LocationRoleType_GREENHOUSE: URIRef  # A location where plants are grown and cultivated, within an enclosed or semi-enclosed environment, often within a covered indoor space. Includes temporary or semi-permanent structures.
    LocationRoleType_GROCERY: URIRef  # An area where household grocery products, such as fresh or shelf stable foods, domestic cleaning supplies, personal hygiene items, for example, that are displayed in stores on standard shelving.
    LocationRoleType_HANDLING_AREA: URIRef  # An operational area where internal activities associated with storing, moving, protecting or other handling of goods take place throughout the processes of manufacturing, warehousing or distribution.
    LocationRoleType_HEAD_OFFICE: URIRef  # A location that serves as the executive or main office of an organization.
    LocationRoleType_HOSPITAL: URIRef  # A location where health care organizations provide patient treatment with specialised medical and nursing staff, medical equipment and inpatient care facilities.
    LocationRoleType_HOSPITAL_CAFETERIA: URIRef  # A restaurant within a hospital or other medical facility in which the customers serve themselves or are served at a counter.
    LocationRoleType_HOSPITAL_DEPARTMENT: URIRef  # An area within a hospital which provides specific treatment or support services  not individually included in the Location Type list.
    LocationRoleType_HOSPITAL_PHARMACY: URIRef  # A location within a hospital where pharmaceuticals or medical devices can be dispensed by a pharmacy operator to hospital staff for inpatient treatment as well as directly to patients being discharged. Differs to a retail pharmacy as the site may be related to government funding, subsidized reimbursement lists or agencies, and may also dispense specialized pharmaceuticals (e.g., orphan drugs).
    LocationRoleType_IMAGING_DIAGNOSTICS_AREA: URIRef  # An area within a healthcare facility, usually a hospital or radiology facility, designated for the purpose of imaging and diagnostics.
    LocationRoleType_IMPREST_LOCATION: URIRef  # Usually a ward-level location in which stock is held for use on that ward.
    LocationRoleType_INLAND_FISHERY: URIRef  # A location devoted to the rearing and harvesting of aquatic animals and plants within an inland freshwater ecosystem (i.e., fresh or limnetic waters) for industrial, small-scall/artisanal or recreational purposes. Includes natural flowing or lotic waters such as rivers or streams (including their smaller elements such as springs, brooks, rivulets, or rills), artificial canals, and static or lentic waters such as natural lakes and tarns and artificial lakes or reservoirs such as rivers, lakes, etc.
    LocationRoleType_INLAND_PORT: URIRef  # A location with permanent facilities, situated along inland waterways, where inland waterway ships and vessels may dock to receive services such as loading and discharging passengers, crews or cargo, refuelling, restocking, etc.
    LocationRoleType_INTERMODAL_TERMINAL: URIRef  # A location that is a specific type of terminal, which supports the transfer between various modes of transport such as rail, road, maritime, inland waterways.
    LocationRoleType_INTERNATIONAL_MAIL_PROCESSING_CENTER: URIRef  # A location with mail processing facilities recognized by the Universal Postal Union (UPU) that generates or receives dispatches and/or acts as a transit center for mail exchanged between other International Mail Processing Centers (IMPC).
    LocationRoleType_LANE_OR_ROUTE: URIRef  # A specific transportation lane or route.
    LocationRoleType_LAY_AWAY: URIRef  # An area within a store for holding or consolidating customer purchases for final payment and pickup.
    LocationRoleType_LIBRARY: URIRef  # A building or room containing collections of books, periodicals, and sometimes films and recorded music for use or borrowing by the public or the members of an institution.
    LocationRoleType_MAIN_RECEPTION: URIRef  # An area within a facility, often near the entrance, that is used predominantly to greet visitors to the building.
    LocationRoleType_MANUFACTURING_PLANT: URIRef  # A location consisting of one or more buildings with facilities for manufacturing.
    LocationRoleType_MARINE_FISHERY: URIRef  # A location devoted to the rearing and harvesting of aquatic animals and plants within a marine saltwater ecosystem (i.e., open sea/pelagic zone), for industrial, small-scall/artisanal or recreational purposes.
    LocationRoleType_MARKET: URIRef  # A location where multiple sellers can set-up mobile stalls, booths or stores, to sell various goods to consumers. Markets often include a wide variety of goods such as fresh produce, handcrafts, artisan products for example, and may also include 'pop-up' type stores that are temporary or move from market to market.
    LocationRoleType_MENTAL_HEALTH_SERVICE: (
        URIRef  # Provides mental health treatment and support services.
    )
    LocationRoleType_MILKING_SITE: URIRef  # Milking is the act of removing milk from mammary glands of various animal types.
    LocationRoleType_MOBILE_READER: URIRef  # Any non-fixed (portable) reader configuration (reader and antennas) for the purpose of capturing EPC data (e.g. Hand held or forklift reader).
    LocationRoleType_NURSE_STATION: (
        URIRef  # Nurse station within a hospital or other healthcare service provider
    )
    LocationRoleType_OFFICE: URIRef  # A room, set of rooms, or building where the business of a commercial or industrial organization or an individual professional is conducted.
    LocationRoleType_ONLINE_PLATFORM: URIRef  # A digital location offering online services that utilize the internet to facilitate interactions between two or more distinct but interdependent sets of users. Includes graphical user interfaces for human interaction and/or system interfaces for connection with other digital services (e.g., APIs). Examples include search engines, marketplaces, online financial systems, distribution management entities (DME) etc.
    LocationRoleType_ONLINE_SHOP: URIRef  # A digital location where a varied selection of goods or services can be sold to a consumer, by a single seller who may also operate physical stores offering the same varied selection of goods or services under their own brand name or from different brands. Differs to an online platform marketplace, which enables multiple sellers to offer goods and services through the same platform.
    LocationRoleType_OPERATING_THEATER: URIRef  # A facility usually within a hospital used to perform medical/surgical procedures.
    LocationRoleType_PACKAGING_AREA: (
        URIRef  # An area within a facility where product is packaged.
    )
    LocationRoleType_PACKHOUSE: URIRef  # A location (standalone or part of a larger facility) where fresh foods such as fruit, vegetables, grains, meat or horticultural products, for example, are sorted, prepared and packed ahead of distribution to shops or markets for sale to end users.
    LocationRoleType_PALLET_WRAPPER: URIRef  # An area where any automatic or manual method using bands of plastic film applied to product  used to encase palletised loads prior to shipment to protect against product damage.
    LocationRoleType_PATHOLOGY: (
        URIRef  # Pathology area within a hospital or independently operated.
    )
    LocationRoleType_PERSONAL_SERVICES: URIRef  # Business providing personal services such as beauty therapy, tattoo parlours, hair salons etc.
    LocationRoleType_PETROL_STATION: (
        URIRef  # An establishment beside a road selling fuel for motor vehicles.
    )
    LocationRoleType_PICK_UP_LOCATION: URIRef  # A location where goods may be temporarily stored until collected or loaded to a shipment for the next part of a transportation process.
    LocationRoleType_PICKING_AREA: URIRef  # An area within a facility in which product is picked to fulfil an order.
    LocationRoleType_POINT_OF_SALE: URIRef  # An area, usually within a store, commonly known as a 'checkout', where barcodes on trade items can be scanned to enable a consumer purchase and to complete and record the transaction for the seller.
    LocationRoleType_PRIMARY_HEALTH_SERVICE: URIRef  # A health service which provides a first point of consultation for patients. Includes community centres.
    LocationRoleType_PRINTING_ROOM: URIRef  # An area which provides printed labels/tags for  the goods/cartons/pallets within a DC or manufacturer facility.
    LocationRoleType_PRODUCTION_AREA: URIRef  # An area within a facility where the conversion of materials and or assembly of components to manufacture goods, products or services takes place.
    LocationRoleType_PRODUCTION_LINE: URIRef  # An area in a factory in which goods being manufactured is passed through a set linear sequence of mechanical or manual operations.
    LocationRoleType_PROMOTION_AREA: URIRef  # A specific area or room that is used to hold special purchased product.
    LocationRoleType_PUBLIC_WAREHOUSE: URIRef  # A building, or a part of one, where storage space is offered to other companies for compensation (fee), for the storage of their goods, merchandise, etc.
    LocationRoleType_QUALITY_CONTROL: URIRef  # An area in which any product not meeting quality standards is held pending further evaluation.
    LocationRoleType_QUARANTINE: URIRef  # An area at a manufacturing, distribution or retail facility to hold product that may not be suitable for consumption until further inspection.
    LocationRoleType_RAIL_STATION: URIRef  # A location with one or more buildings/platforms where trains can stop for people to embark and disembark.
    LocationRoleType_RAIL_TERMINAL: URIRef  # A location with one or more railway terminals such as freight terminals or rail stations (excluding passenger terminals), that provides connections with other rail vehicles and other modes of transport.
    LocationRoleType_READ_POINT_VERIFICATION_SPOT: URIRef  # A point at which a tagged object's location has been verified by an associated read of a separate fixed location tag. Read Point Verification Spot would be used when there is a business process to capture the current location of an object at rest (typically with a mobile reader).
    LocationRoleType_REARING_AREA: URIRef  # The place the animal was raised after birth to the end of the animals' life. Note: the term animal includes but is not limited to mammals, birds, fish and crustaceans.
    LocationRoleType_RECALLED_PRODUCT_AREA: URIRef  # An area in which recalled product is stored pending shipment back to the manufacturer or the manufacturer's designated returns centre for final disposition.
    LocationRoleType_RECEIVING_AREA: URIRef  # An area within a facility where incoming goods are unloaded and checked for condition and completeness.
    LocationRoleType_RECEIVING_LOCATION: URIRef  # A location where goods may be temporarily received and stored for the purpose of unloading shipments.
    LocationRoleType_REPACKING_FACILITY: URIRef  # A location where goods may be combined with other goods and packed for sale or shipping distribution as a single pack. For locations where transport units are combined for shipping, see CONSOLIDATING_CENTER.
    LocationRoleType_RESEARCH_FACILITY: (
        URIRef  # An institute,  centre, or other location where research is conducted.
    )
    LocationRoleType_RESIDENCE: URIRef  # A dwelling or an apartment where one lives.
    LocationRoleType_RETAIL_PHARMACY: URIRef  # A location for a retail store that sells and/or dispenses pharmaceuticals and medical devices to the general public, often at the direction of physicians. Quite often also sells personal care goods, toiletries and non-controlled or over-the-counter (OTC) drugs.
    LocationRoleType_RETURNABLE_ASSET_SERVICE_CENTER: (
        URIRef  # The location where a returnable asset is serviced.
    )
    LocationRoleType_RETURNS_AREA: URIRef  # An area where goods, that have been dispatched to be delivered, are received back into a facility for further processing. Examples of processing include sorting, cleaning, resale, onward transportation to other specialized facilities, destruction, etc.
    LocationRoleType_ROAD_TERMINAL: (
        URIRef  # A location that is connected to other locations by means of roads.
    )
    LocationRoleType_SALES_FLOOR: URIRef  # An area within a store (all formats -  club, etc.) where product is displayed for customer purchase.
    LocationRoleType_SALES_FLOOR_TRANSITION_AREA: URIRef  # An area within a store between two physical locations (e.g. Backroom and Sales Floor) - used for a read point only.
    LocationRoleType_SALES_YARD: (
        URIRef  # A location for individuals or companies to sell used goods.
    )
    LocationRoleType_SEAPORT: URIRef  # A location with maritime facilities, at which both seagoing and inland waterway ships and seagoing vessels may dock to receive services such as loading and discharging passengers, crews or cargo, refuelling, restocking, repair.
    LocationRoleType_SECURITY_AREA: URIRef  # A designated internal location for the purpose of minimising direct access to the product.
    LocationRoleType_SELF_SERVICE: URIRef  # The product should be placed in an area where the consumer can self serve themselves to their purchase needs. The product may have been portioned, cut or modified prior.
    LocationRoleType_SERVICE_COUNTER: URIRef  # The product is recommended to be placed at a location where an employee from the trading partner will need to portion, cut, or modify the product to the end consumer based upon consumer need.
    LocationRoleType_SHELF: URIRef  # A location specified within a larger area, used to hold or store objects. A shelf is generally a flat, rigid surface or structure which may usually be composed of wood, glass or metal, fixed at right angles to a wall or other vertical structure.
    LocationRoleType_SHIPPING_AREA: URIRef  # An area within a facility where outgoing goods are checked for condition and completeness and loaded onto a conveyance for transport.
    LocationRoleType_SHIP_FROM_LOCATION: URIRef  # The location from which physical goods are shipped. In cases when a shipment may be completed through a single consignment, the ship from location is the same location that is managed by the dispatch party or used by the consignor. However in cases when a shipment involves multiple consignments, there will various ship from locations, that do not necessarily correspond to the same locations associated with the consignors or dispatch parties.
    LocationRoleType_SHIP_TO_LOCATION: URIRef  # The location to which physical goods are shipped. In cases when a shipment may be completed through a single consignment, the ship to location is the same location that is managed by the delivery recipient party or used by the consignee. However in cases when a shipment involves multiple consignments, there will be various ship to locations, that do not necessarily correspond to the same locations associated with the consignees or delivery recipient parties.
    LocationRoleType_SILO: URIRef  # A location or area within a larger location, used to store grain within a tower or pit.
    LocationRoleType_SLAUGHTER_HOUSE: (
        URIRef  # A facility where animals are slaughtered for meat as food.
    )
    LocationRoleType_SPORTS_AND_RECERATIONAL: URIRef  # A location for individuals to engage in sports and recreational activities for leisure.
    LocationRoleType_STAGING_AREA: URIRef  # A location where goods may be stored temporarily between two separate stages or parts of an overall inbound or outbound goods process. E.g., received and approved goods may sit in a staging area before they are put away into the main storage area of the warehouse. Another example is when components for a manufacturing process are temporarily placed in a staging area between the warehouse and the manufacturing shop floor until those components can be taken to the correct workstations on the manufacturing shop floor.
    LocationRoleType_STATION: URIRef  # An establishment or building where a specified activity or service is based.
    LocationRoleType_STORAGE_AREA: URIRef  # An area within a facility where material or goods are kept to fulfil a future need. Examples of facilities include shops, manufacturing plants, distribution centers, yards, depots, etc.
    LocationRoleType_STORE: URIRef  # A location where a varied selection of goods or services can be sold to a consumer.
    LocationRoleType_TERMINAL: URIRef  # A location which serves as a pathway for handling transport processes that may involve cargo and people, such as passengers or crew, for example.
    LocationRoleType_TRADE_ITEM_RETURN_LOCATION: URIRef  # A code to qualify the locations to which a retailer or wholesaler can send unsold product. Examples are expired product, damaged, reclamation or general product returns.
    LocationRoleType_TRAIN: URIRef  # A form of rail transport consisting of a series of connected vehicles that generally run along a railroad (or railway) track to transport passengers or cargo (also known as 'freight' or 'goods').
    LocationRoleType_VENDING: (
        URIRef  # The retailing merchandise through vending machines.
    )
    LocationRoleType_VENDOR_LEASED_SPACE: URIRef  # A trade channel where the trade item is sold through a retailer within a retailer for example a rack jobber.
    LocationRoleType_VINEYARD: (
        URIRef  # An area where grape vines are grown in order to produce wine.
    )
    LocationRoleType_VISITING_ADDRESS: URIRef  # An enterprise's physical location where guests are received during set working hours.
    LocationRoleType_WARD: URIRef  # Usually, a sub-location within a hospital typically one allocated to a particular type of patient.
    LocationRoleType_WAREHOUSE: URIRef  # A location equipped with the appropriate equipment and fittings for large quantities of items such as raw materials or manufactured goods to be stored in the appropriate conditions prior to distribution e.g., cold storage. A warehouse is a facility that, along with appropriate storage and handling equipment includes personnel and management resources, enabling to stocking or storage of goods and control of inbound goods (e.g., such as those received from suppliers, production centets, etc.) and outbound goods (e.g., such as those being sent to production, sales, etc.).
    LocationRoleType_WASTE_CENTER: URIRef  # An area within a parent location designated for the central depositing of waste streams prior to collection.
    LocationRoleType_WHARF: URIRef  # A wharf or quay is a fixed location with a structure built parallel to the waterfront of a harbour, navigable river or any body of water so that ships and vessels may lie alongside for docking, loading, and unloading purposes.
    LocationRoleType_YARD: URIRef  # A tract of ground next to, surrounding, or surrounded by a building or buildings, used for holding product (e.g., ores, sand) or equipment (e.g. trailer, container, wagons) or transport means (e.g., trucks, tractors, locomotives).
    LocationStatusHistory: URIRef  # Over the lifetime of a location, it may go through periods of being active and inactive. gs1:LocationStatusHistory allows changes in status to be communicated in advance and tracked over time.
    Luminance: URIRef  # A measure of the light-emitting intensity of a light source, in a specific direction per unit area of the emitting surface. For a very narrow cone containing the direction, it is the ratio of the luminous flux emitted within that cone to the solid angle of the cone per unit area of the emitting surface.  SI Units: candela per square metre
    LuminousFlux: URIRef  # A measure of the perceived power of light emitted by a source or received by a surface and irrespective of direction, taking into account the sensitivity of the human eye to different wavelengths of light.  SI Units: lumen = 1 candela per steradian
    LuminousIntensity: URIRef  # A measure of the light-emitting intensity of a light source, in a specific direction. For a very narrow cone containing the direction, it is the ratio of the luminous flex emitted within that cone to the solid angle of the cone.  SI Units: candela
    MagneticFlux: URIRef  # A measure of the total magnetic field that passes through a specific area. The surface integral of the product of the permeability of the medium and the magnetic field intensity perpendicular to the surface.  SI Units: weber
    MagneticFluxDensity: URIRef  # The product of the magnetic field strength and the permeability of a material.  SI Units: tesla = weber per square metre
    MagneticVectorPotential: URIRef  # The potential energy per unit element of current (current multiplied by length).    SI Units: weber per metre  (Joules per ampere metre)
    Mass: URIRef  # The quantity of matter in a body. Inertial mass is the measure of the inertia of a body; its resistance to acceleration.  SI Units: kilogram
    MassConcentration: URIRef  # The mass of the consistutent (or solute) divided by the volume of the mixture (or solvent).  SI Units: kilogram per cubic metre
    MassFlowRate: URIRef  # The mass of fluid that passes per unit of time.  SI Units: kilogram per second
    MassPerAreaTime: URIRef  # The mass of fluid that passes per unit of time per unit area perpendicular to the flow direction.  SI Units: kilogram per second per square metre
    MaturationMethodCode: URIRef
    MaturationMethodCode_JET_FRESH: URIRef  # Freshly picked and immediately packed and shipped at mature stage and flown to destination for adequate distribution (i.e. imports from South America, Africa or Europe). Flown by jet to market; the carton will be labelled Jet Fresh, when applicable, stickered Jet Fresh. For the produce industry, most common with berries, stone fruits and pineapples.
    MaturationMethodCode_PRECONDITIONED: URIRef  # Product stored at proper temperature prior to shipment to allow ripening and/or colouring, adequate for distribution and/or consumption. Pre-conditioned product is matured to a specific maturity level as a result of ripening through either temperature, gas treatment, humidity or any combination thereof.
    MaturationMethodCode_TREE_VINE_RIPE: URIRef  # Product that is picked at optimum maturity or just shy of. It is almost ripe or ready to eat. This fruit will be shipped immediately (imported = flown) from the pack-house and stickered as Tree or Vine Ripe.
    MeasurementPrecisionCode: URIRef
    MeasurementPrecisionCode_APPROXIMATELY: URIRef  # The method used to analyse the products resulted in approximate value of the nutritional content.
    MeasurementPrecisionCode_EXACT: URIRef  # The method used to analyse the products resulted in exact value of the nutritional content.
    MeasurementPrecisionCode_LESS_THAN: URIRef  # To indicate presence when the measurement value is too small to be measured precisely (rule states less than 0.5).
    MeasurementType: URIRef  # A set of measurement types for properties that can be measured or sensed by appropriate measuring devices or sensors
    MeatPoultry: URIRef  # Meat and poultry products.
    MemoryCapacity: URIRef  # A measure of the size of a data structure or capacity of a data carrier, typically measured in bits (binary digits), bytes or octets (8 bits) or multiples thereof.  Units: byte
    MilkButterCreamYogurtCheeseEggsSubstitutes: URIRef  # Milk butter cream yogurts cheese eggs and any substitutes for these products.
    MolalityOfSolute: URIRef  # The concentration of a solution expressed as the number of moles of dissolved substance per unit mass of solvent.  SI Units: mole per kg
    MolarEnergy: URIRef  # The ratio of the thermodynamic energy of a chemical compound to the amount of substance (atoms or molecules) contained within it, the amount of substance being measured in moles.  SI Units: joule per mole
    MolarMass: URIRef  # The ratio of the mass of a chemical compound to the amount of substance (atoms or molecules) contained within it, the amount of substance being measured in moles.  SI Units: kilogram per mole
    MolarVolume: URIRef  # The volume occupied by a substance per unit amount of substance at a specified temperature and pressure.  SI Units: cubic metre per mole
    NonbinaryLogicCode: URIRef
    NonbinaryLogicCode_FALSE: URIRef
    NonbinaryLogicCode_NOT_APPLICABLE: URIRef
    NonbinaryLogicCode_TRUE: URIRef
    NonbinaryLogicCode_UNSPECIFIED: URIRef
    NutrientBasisQuantityCode: URIRef
    NutrientBasisQuantityCode_BY_MEASURE: URIRef  # Nutrient measurement is based on a measurement value for example grams or ounces.
    NutrientBasisQuantityCode_BY_SERVING: (
        URIRef  # Nutrient measurement is based on a specified serving amount.
    )
    NutritionMeasurementType: (
        URIRef  # A class providing nutritional value and intake percent.
    )
    NutritionalClaimTypeCode: URIRef
    NutritionalClaimTypeCode_ADDITIVE_FREE: URIRef  # A claim that a food is free from additives. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_ARTIFICIALLY_SWEETENED: URIRef  # A claim that a food contains artificial sweeteners. Artificial sweeteners are sugar substitutes that are synthetic.
    NutritionalClaimTypeCode_CHOLESTEROL_FREE: URIRef  # A claim that a food is free from Cholesterol. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_COLOURING_AGENT_FREE: URIRef  # A claim that a food is free from colouring agents. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_CONTAINS_GLYZYRRHIZIN: URIRef  # A claim that a food contains glyzyrrhizin. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_CONTAINS_LIQUORICE: URIRef  # A claim that a food is contains liquorice. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_CONTAINS_SOY: URIRef  # A claim that a food contains soy. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_EGG_FREE: URIRef  # A claim that a food is free from egg. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_ENERGY_FREE: URIRef  # A claim that a food is energy-free, and any claim likely to have the same meaning for the consumer, may only be made where the product contains less than 4kcal (17kj)/100ml. In the case of energy-free foods, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_ENERGY_REDUCED: URIRef  # A claim that a food is energy-reduced, and any claim likely to have the same meaning for the consumer, may only be made where the energy value is reduced by at least 30%, with an indication of the characteristic(s), which make(s) the food reduced in its total energy value.
    NutritionalClaimTypeCode_ENRICHED_OR_FORTIFIED_IN_VITAMINS_AND_OR_MINERALS: URIRef  # A claim that a food is enriched or fortified in vitamins and/or minerals, and any claim likely to have the same meaning for the consumer, may only be made where the product contains the vitamins and/or minerals in at least a significant amount as defined in the Annex of Directive 90/496/EEC.
    NutritionalClaimTypeCode_FAT_FREE: URIRef  # A claim that a food is fat-free, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.5g of fat per 100g or 100ml. However, claims expressed as X% fat-free shall be prohibited. In the case of foods naturally fat-free, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_FREE_FROM_GLUTEN: URIRef  # A claim that a food is free from Gluten. Any claim likely to have the same meaning for the consumer, may only be made where the product contains an amount less than or equal to 20 mg/kg gluten according to the Commission Regulation (EC) No 41/2009
    NutritionalClaimTypeCode_GUARANTEED_LACTOSE_FREE: URIRef  # A claim that a food is regularly analysed to guarantee that the product is free from lactose.
    NutritionalClaimTypeCode_HIGH_FIBRE: URIRef  # A claim that a food is high in fibre, and any claim likely to have the same meaning for the consumer, may only be made where the product contains at least 6g of fibre per 100g or at least 3g of fibre per 100 kcal. In the case of foods naturally high in fibre, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_HIGH_PROTEIN: URIRef  # A claim that a food is high in protein, and any claim likely to have the same meaning for the consumer, may only be made where at least 20% of the energy value of the food is provided by protein. In the case of foods naturally high in protein, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_HIGH_VITAMINS_AND_OR_MINERALS: URIRef  # A claim that a food is high in vitamins and or minerals, and any claim likely to have the same meaning for the consumer, may only be made where the product contains at least twice the value of source of vitamins and minerals. In case of foods naturally high in vitamins and/or minerals, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_LACTOSE_FREE: URIRef  # A claim that a food is free of lactose. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_LIGHT_LITE: URIRef  # A claim stating that a product is light or lite, and any claim likely to have the same meaning for the consumer, shall follow the same conditions as those set for the term reduced; the claim shall also be accompanied by an indication of the characteristic(s) which make the food light or lite.
    NutritionalClaimTypeCode_LOW_ENERGY: URIRef  # A claim that a food is low in energy, and any claim likely to have the same meaning for the consumer, may only be made where the product contains less than 40 kcal (170 kj)/100g and less than 20kcal (80kj)/100ml. In the case of foods naturally low in energy, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_LOW_FAT: URIRef  # A claim that a food is low in fat, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 3g of fat per 100g or 1.5g of fat per 100ml. In the case of foods naturally low in fat, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_LOW_LACTOSE: URIRef  # A claim that a food is low in lactose. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_LOW_PROTEIN: URIRef  # A claim that a food contains low levels of protein. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_LOW_SATURATED_FAT: URIRef  # A claim that a food is low in saturated fat, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 1.5g of saturates per 100g for solids or, 0.75g of saturates per 100ml for liquids and in either case saturated fat must not provide more than 10% of energy. In the case of foods naturally low in saturated fat, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_LOW_SODIUM_SALT: URIRef  # A claim that a food is low in sodium, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.12g of sodium, or the equivalent value for salt, per 100g or per 100ml. In the case of foods naturally low in sodium, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_LOW_SUGARS: URIRef  # A claim that a food is low in sugars, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 5g of sugars per 100g or 100ml. In the case of foods naturally low in sugars, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_MILK_FREE: URIRef  # A claim that a food is free from milk. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_MILK_PROTEIN_FREE: URIRef  # A claim that a food is free from milk proteins. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_NATURAL_SOURCE_OF_VITAMINS_AND_OR_MINERALS: URIRef  # A claim that a food is a natural source of vitamins and/or minerals, and any claim likely to have the same meaning for the consumer, may only be made where the product contains at least 15% of the recommended daily allowance specified in the Annex of Council Directive 90/496/EEC per 100 g or 100 ml.
    NutritionalClaimTypeCode_NON_ALCOHOLIC: URIRef  # A claim that a food contains no alcohol. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_NUT_FREE: URIRef  # A claim that a food is free from nuts. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_PEANUT_FREE: URIRef  # A claim that a food is free from peanuts. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_PRESERVATIVE_FREE: URIRef  # A claim that a food is free from preservatives. A preservative is a natural or synthetic substance or chemical that is added to products to prevent decomposition by microbial growth or by undesirable chemical changes. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_SATURATED_FAT_FREE: URIRef  # A claim that a food does not contain saturated fat, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.1g of saturated fat per 100g or 100ml. In the case of foods naturally saturated fat-free, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_SODIUM_FREE_OR_SALT_FREE: URIRef  # A claim that a food is sodium-free, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.005g of sodium, or the equivalent value for salt, per 100g. In the case of foods naturally sodium-free, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_SOURCE_OF_FIBRE: URIRef  # A claim that a food is a source of fibre, and any claim likely to have the same meaning for the consumer, may only be made where the product contains at least 3g of fibre per 100g or at least 1.5g of fibre per 100kcal. In the case of foods that are naturally sources of fibre, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_SOURCE_OF_PROTEIN: URIRef  # A claim that a food is a source of protein, and any claim likely to have the same meaning for the consumer, may only be made where at least 12% of the energy value of the food is provided by protein. In the case of foods that are naturally sources of protein, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_SOY_FREE: URIRef  # A claim that a food is free from Soy. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_STRONGLY_SALTED: URIRef  # A claim that a food has a high sodium content. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_SUGARS_FREE: URIRef  # A claim that a food is sugars-free, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.5g of sugars per 100g or 100ml. In the case of foods naturally sugars-free, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_SWEETENED_WITH_AGAVE_SYRUP: (
        URIRef  # A claim that a food is sweetened with syrup from the Agave plant.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_CANE_SUGAR: (
        URIRef  # A claim that a food is sweetened with sugar from sugar cane.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_CORN_SYRUP: (
        URIRef  # A claim that a food is sweetened with corn syrup.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_FRUCTOSE: (
        URIRef  # A claim that a food is sweetened with fructose.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_FRUIT_JUICE: (
        URIRef  # A claim that a food is sweetened with fruit juice.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_FRUIT_SYRUP: URIRef  # A claim that a food is sweetened with fruit syrup. Fruit syrup is made from fruit and other ingredients such as sugar, corn syrup and water.
    NutritionalClaimTypeCode_SWEETENED_WITH_HONEY: (
        URIRef  # A claim that a food is sweetened with honey.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_MALT: (
        URIRef  # A claim that a food is sweetened with malt.
    )
    NutritionalClaimTypeCode_SWEETENED_WITH_RAW_BEET_SUGAR: URIRef  # A claim that a food is sweetened with raw sugar derived from the sugar beet.
    NutritionalClaimTypeCode_SWEETENED_WITH_WHITE_SUGAR: URIRef  # A claim that a food is sweetened with white sugar. White or granulated sugar is refined sugar (pure white crystalline sucrose) ground to granules or grains.
    NutritionalClaimTypeCode_VERY_LOW_GLUTEN: URIRef  # A claim that a food contains a low level of gluten which is defined as 21 - 100 mg/kg gluten according to the Commission Regulation (EC) No 41/2009
    NutritionalClaimTypeCode_VERY_LOW_SODIUM_SALT: URIRef  # A claim that a food is very low in sodium, and any claim likely to have the same meaning for the consumer, may only be made where the product contains no more than 0.04g of sodium, or the equivalent value for salt, per 100g or per 100 ml. In the case of foods naturally very low in sodium, the term naturally may be used as a prefix to this claim.
    NutritionalClaimTypeCode_WHEAT_FREE: URIRef  # A claim that a food is free from wheat. Note the amount that determines containment or lack of containment is based on target market regulations.
    NutritionalClaimTypeCode_WITH_NO_ADDED_SUGARS: URIRef  # A claim stating that sugar has not been added to a food, and any claim likely to have the same meaning for the consumer, may only be made where the product does not contain any added mono- or disaccharides or any other food used for its sweetening properties.
    Offer: URIRef  # An offer to transfer some rights to an item or to provide a service,for example, an offer to sell tickets to an event, to rent the DVD of a movie, to stream a TV show over the internet, to repair a motorcycle, or to loan a book.
    OfferRedemptionTypeCode: URIRef
    OfferRedemptionTypeCode_COUPON_CODE: URIRef  # Offer available as a code that can be entered to redeem the coupon or voucher.
    OfferRedemptionTypeCode_GIFT_CARD: URIRef  # A prepaid stored-value money card.
    OfferRedemptionTypeCode_REBATE: (
        URIRef  # A partial refund upon purchase of a product.
    )
    OfferRedemptionTypeCode_SALE: (
        URIRef  # Offer available as a reduced sales price on a product.
    )
    OfferRedemptionTypeCode_SINGLE_USE_CODE: URIRef  # Offer available as a code that can be entered once to redeem the coupon.
    OrganicClaimAgencyCode: URIRef
    OrganicClaimAgencyCode_1: URIRef  # EPA - US Environmental Protection Agency
    OrganicClaimAgencyCode_10: URIRef  # Demeter-Bund - The Demeter movement as an entrepreneurial network promotes the development of bio-dynamic economy, to secure the livelihoods of the world and to strengthen the positive people in his ministry. In cooperation contribute producers, processors, traders and consumers in partnership to shape the market.
    OrganicClaimAgencyCode_11: URIRef  # GÄA - GÄA is a diverse farming association for farmers, processors and traders inside.Focal point is Germany. Gäa is a special design for the structure of the organic farming.  Biokreis- The Biokreis is an association for organic farming. Currently more than 800 farms, 80 and 200 processors, consumers are members of Biokreis, committed to working together on more than 33,000 for organic and sustainable farming.
    OrganicClaimAgencyCode_12: URIRef  # Naturland - Naturland is active the world over in promoting organic agriculture. Its members are farmers who produce a wide range of valuable products: coffee from Mexico and Peru, olive oil from Greece, tea from the slopes of India's mountains, pineapple and other tropical fruit from Uganda, spices from Sri Lanka. Organic agriculture safeguards the existence of smallholders and helps with the sustainable management of what are often fragile ecosystems. On a global scale, over 50,000 Naturland farmers are cultivating an area of over 142,000 hectares.
    OrganicClaimAgencyCode_13: URIRef  # Biopark - Biopark is an organic farmers' association based in the North of Germany, in Mecklenburg-Vorpommerania.
    OrganicClaimAgencyCode_14: URIRef  # Ecovin - ECOVIN Federation Organic Viticulture Association: ECOVIN largest merger in 1985 as ecologically-working wine estates in Germany was founded. Approximately 220 member companies currently manage 1,600 hectares of vineyards in 11 German wine-growing areas.
    OrganicClaimAgencyCode_15: URIRef  # IFOAM - The International Federation of Organic Agriculture Movements (IFOAM) is a grassroots and democratic organisation that currently unites 750 member organisations in 116 countries. Note: this value will be deleted in the future and should not be used.
    OrganicClaimAgencyCode_16: URIRef  # Demeter International Demeter-International e. V. is a non profit organisation and its member organisations work together in the spirit of an international confederation with democratic principles. Membership requires a functioning Demeter certification programme.
    OrganicClaimAgencyCode_17: URIRef  # Bioland: The leading organic farmers' association in Germany for the economy of organic-based businesses without synthetic pesticides and synthetic chemical nitrogen fertilizer. The animals are kept humanely and processed food carefully. This provides an environmentally sound and sustainable food production. http://www.bioland.de.
    OrganicClaimAgencyCode_19: URIRef  # Quality Certification Services. Note: this value will be deleted in the future and should not be used.
    OrganicClaimAgencyCode_2: URIRef  # FSA - UK Food Standards Agency
    OrganicClaimAgencyCode_20: URIRef  # Washington State Dept. of Agriculture. Note: this value will be deleted in the future and should not be used.
    OrganicClaimAgencyCode_21: URIRef  # The Canada Organic Regime is the Government of Canada's response to requests by the organic sector and consumers to develop a regulated system for organic agricultural products. The Organic Products Regulations define specific requirements for organic products to be labelled as organic or that bear the Canada Organic logo. URL: http://www.inspection.gc.ca/food/organic-products/labelling-and-general-information/certified-choice/eng/1328082717777/1328082783032
    OrganicClaimAgencyCode_22: URIRef  # The European Union Commission.
    OrganicClaimAgencyCode_23: URIRef  # OISCC - The Organic Industry Standards and Certification Council maintains the Australian National Standard for Organic and Biodynamic Produce, to ensure continued consumer confidence and International market access.
    OrganicClaimAgencyCode_24: URIRef  # ACO - Australian Certified Organic is Australia's largest certifier for organic and biodynamic produce and has over 1500 operators within its certification system. ACO is a not for profit fully-owned subsidiary of Australia Organic Ltd.
    OrganicClaimAgencyCode_25: URIRef  # NASAA Certified Organic (NCO) is a fully-owned subsidiary of The National Association for Sustainable Agriculture, Australia who provides the certification services.
    OrganicClaimAgencyCode_26: URIRef  # OFC - The Organic Food Chain provides certification services in accordance with the National Standard for Organic and Bio-Dynamic Produce and other international organic certification standards.
    OrganicClaimAgencyCode_27: URIRef  # AUS-QUAL is a certification body accredited by JAS-ANZ, providing conformity assessment services for quality management and food safety (HACCP) management systems, as well as Product Cortication Systems for the wider Australian and New Zealand agricultural, horticultural and secondary processing sectors.
    OrganicClaimAgencyCode_28: URIRef  # The Bio-Dynamic Research Institute, founded in 1957, is involved in research and practical development of the Australian DEMETER Bio-Dynamic Method of Agriculture. In 1967 it was vested with the rights and supervision of the DEMETER Trademark in Australia. Part of this role is the certification of DEMETER quality products.
    OrganicClaimAgencyCode_29: URIRef  # Safe Food Production Queensland  works in partnership with the Department of Agriculture and Fisheries and Forestry (DAFF) and Queensland Health (QH) across the entire food chain, to ensure Queensland's food supply is safe.
    OrganicClaimAgencyCode_3: URIRef  # FDA - US Food and Drug Agency
    OrganicClaimAgencyCode_30: URIRef  # The Danish Veterinary and Food Administration (DVFA) is part of the Ministry of Environment and Food. DVFA is responsible for food safety and health from farm to fork and maintains a list of Danish food companies, aquacultural farms etc. subject to organic inspection. Only authorities under the Ministry of Environment and Food carry out inspection under the government rules for organic production. The Danish AgriFish Agency inspects the primary production, while the Danish Veterinary and Food Administration (DVFA) inspects food companies.
    OrganicClaimAgencyCode_31: URIRef  # Verbund Ökohöfe e.V. is an organic cultivation association based in Wanzleben in the Magdeburg Börde region
    OrganicClaimAgencyCode_32: URIRef  # The biolabel of the Bavarian State Ministry for Food, Agriculture and Forestry meets the wish of consumers for a high quality of organic products and traceable origin. Only those products whose organic quality standards extend far beyond the statutory regulations and originate from the stated regions are permitted to bear this quality seal. Try out convincing organic products yourself, safe in the knowledge of their place of origin.
    OrganicClaimAgencyCode_33: URIRef  # The products marked with the bio-symbol Baden-Württemberg are regional organic foods with traceable origin. The use or labelling is based on the ecological standards of the EC eco-regulation supplemented by the requirement that the products have to be produced in fully converted farms and partly also to the stricter requirements of the ecological cultivation associations
    OrganicClaimAgencyCode_34: URIRef  # The EKO Certification Foundation is an independent private foundation established in 2012. The foundation has no profit objective. The EKO label for foods has been around for 30 years, and most people know as a hallmark for organic foods. The EKO certificate has been the owner of this collective mark. With the advent of the European Ecolabel (the green leaf with the asterisks), EKO has been given the opportunity to develop further. Producers should be in addition to biologically certified, also carry out additional efforts in the area of sustainability.
    OrganicClaimAgencyCode_4: URIRef  # International Foundation for Organic Agriculture
    OrganicClaimAgencyCode_5: URIRef  # BFA - Biological Farmers of Australia
    OrganicClaimAgencyCode_6: URIRef  # USDA- US Department of Agriculture
    OrganicClaimAgencyCode_7: URIRef  # Quality Assurance International www.qai-inc.com QAI is a leading USDA-accredited organic product certifying agency. Note: this value will be deleted in the future and should not be used.
    OrganicClaimAgencyCode_8: URIRef  # Südtirol Bioland - Bioland Association of South Tyrol The Association of South Tyrol is the largest organic association for organic farmers having to farmers in South Tyrol and the only active in association with a national association office Terlan.Note: this value will be deleted in the future and should not be used.
    OrganicClaimAgencyCode_9: URIRef  # Ecoland - Ecoland is a membership organisation whose members elect a governing Board which is responsible for the design and implementation of the organic certification system.
    OrganicClaimAgencyCode_999: URIRef  # Unspecified Agency
    OrganicClaimAgencyCode_BFA: URIRef  # Biological Farmers of Australia
    OrganicClaimAgencyCode_BIOLAND: URIRef  # Bioland: The leading organic farmers' association in Germany for the economy of organic-based businesses without synthetic pesticides and synthetic chemical nitrogen fertilizer. The animals are kept humanely and processed food carefully. This provides an environmentally sound and sustainable food production. http://www.bioland.de.
    OrganicClaimAgencyCode_DEMETER_BUND: URIRef  # The Demeter movement as an entrepreneurial network promotes the development of bio-dynamic economy, to secure the livelihoods of the world and to strengthen the positive people in his ministry. In cooperation contribute producers, processors, traders and consumers in partnership to shape the market.
    OrganicClaimAgencyCode_DEMETER_INTERNATIONAL: URIRef  # Demeter International Demeter-International e. V. is a non profit organisation and its member organisations work together in the spirit of an international confederation with democratic principles. Membership requires a functioning Demeter certification programme. Same as GS1 Code 16
    OrganicClaimAgencyCode_ECOLAND: URIRef  # Ecoland is a membership organisation whose members elect a governing Board which is responsible for the design and implementation of the organic certification system.
    OrganicClaimAgencyCode_ECOVIN: URIRef  # ECOVIN Federation Organic Viticulture Association: ECOVIN largest merger in 1985 as ecologically-working wine estates in Germany was founded. Approximately 220 member companies currently manage 1,600 hectares of vineyards in 11 German wine-growing areas. Same as GS1 code 14
    OrganicClaimAgencyCode_EPA: (
        URIRef  # US Environmental Protection Agency. Same as GS1 Code 1
    )
    OrganicClaimAgencyCode_FDA: URIRef  # FDA US Food and Drug Agency
    OrganicClaimAgencyCode_FSA: URIRef  # UK Food Standards Agency
    OrganicClaimAgencyCode_GAA: URIRef  # GAA is a diverse farming association for farmers, processors and traders inside.Focal point is Germany. GAA is a special design for the structure of the organic farming. Biokreis- The Biokreis is an association for organic farming. Currently more than 800 farms, 80 and 200 processors, consumers are members of Biokreis, committed to working together on more than 33,000 for organic and sustainable farming.
    OrganicClaimAgencyCode_IFOA: (
        URIRef  # International Foundation for Organic Agriculture
    )
    OrganicClaimAgencyCode_IFOAM: URIRef  # The International Federation of Organic Agriculture Movements (IFOAM) is a grassroots and democratic organization that currently unites 750 member organizations in 116 countries. Same as GS1 code 15
    OrganicClaimAgencyCode_NATURLAND: URIRef  # Naturland - Naturland is active the world over in promoting organic agriculture. Its members are farmers who produce a wide range of valuable products: coffee from Mexico and Peru, olive oil from Greece, tea from the slopes of India's mountains, pineapple and other tropical fruit from Uganda, spices from Sri Lanka. Organic agriculture safeguards the existence of smallholders and helps with the sustainable management of what are often fragile ecosystems. On a global scale, over 50,000 Naturland farmers are cultivating an area of over 142,000 hectares.Same as GS1 Code 12
    OrganicClaimAgencyCode_QAI: URIRef  # Quality Assurance International. QAI is a leading USDA-accredited organic product certifying agency.
    OrganicClaimAgencyCode_SUDITIROL: URIRef  # Bioland Association of South Tyrol The Association of South Tyrol is the largest organic association for organic farmers having to farmers in South Tyrol and the only active in association with a national association office Terlan.
    OrganicClaimAgencyCode_USDA: URIRef  # US Department of Agriculture.
    OrganicClaimDetails: URIRef  # A set of organic claim details for the product.
    Organization: URIRef  # An Organization is any legal or physical entity involved at any point in any supply chain and upon which there is a need to retrieve predefined information. An Organization is uniquely identified by a Global Location Number (GLN).
    OrganizationID_Details: URIRef  # Government bodies, trade organisations, and other parties issue identifiers that are associated to legal entities and/or functions. Linking these identifiers to GLN and one another supports consolidating records, mapping related, collaborative identifiers, enhances search ability and enables more efficient transitions between identifiers.  This class provides a mechanism for connecting and sharing party identifiers.
    OrganizationID_Type: URIRef
    OrganizationID_Type_AU_ABN: URIRef  # The Australian Business Number is a unique 11-digit identifier issued by the Australian Business Register which is operated by the Australian Taxation Office.
    OrganizationID_Type_AU_ACN: URIRef  # An Australian Company Number is a unique identifier required by every company registered under Australia's Corporations Act 2001. The ACN is a nine-digit number issued by the Australian Securities & Investments Commission to every Australian company.
    OrganizationID_Type_CRD_PARTNER_CODE: URIRef  # The Central Reference File Database (CRD), formerly known as Central Repository Domain is a centralised database that stores Location Codes and Company Codes required by European regulation, and makes them available to users. CRD contains the following reference files: - List of Countries (ISO 3166) - The Location Reference File which uniquely identifies physical rail points (e.g. stations, customer sidings, loading places) containing the Location Code (which includes the Country Code) - The Partner Reference File uniquely identifies all rail actors who exchange information (Company Codes); Each company actor must have a unique Company Code assigned by UIC
    OrganizationID_Type_CRN: URIRef  # A company registration number is a unique combination of numbers and/or letters. The company registration number (also known as the company number, registration number or simply in its abbreviated form) is used to identify a company and verify that it is an entity registered within the national registry for companies or enterprises. This value is generic and is not associated to any specific region.
    OrganizationID_Type_DID: URIRef  # A globally unique persistent identifier that does not require a centralized registration authority because it is generated and/or registered cryptographically. The generic format of a DID is defined in the DID Core specification [DID-CORE]. A specific DID scheme is defined in a DID method specification. Many (but not all) DID methods make use of distributed ledger technology (DLT) or some other form of decentralized network.
    OrganizationID_Type_DUNS: URIRef  # Data Universal Numbering System. It is a nine-digit numbering system which uniquely identifies an individual business. The DUNS number is a nine-digit number issued by Dun & Bradstreet assigned to each business location in the D&B database having a unique, separate, and distinct operation for the purpose of identifying them. A DUNS number is also a way in which separate corporate entities, having no official relationship, can be branded as one by sharing one DUNS number among the affiliated comp
    OrganizationID_Type_DUNS_PLUS_FOUR: URIRef  # The DUNS+4 refers to the DUNS number assigned by Dun and Bradstreet, plus a 4-character suffix that is assigned by the vendor to establish additional Central Contractor Registration (CCR) database records for identifying alternative electronic funds transfer (EFT) accounts for the same vendor located at the same physical address. Dun and Bradstreet has no affiliation with the 4-character suffix.
    OrganizationID_Type_EORI: URIRef  # Businesses and people wishing to trade with the EU must, use the EORI number as an identification number in all customs procedures when exchanging information with Customs - https://ec.europa.eu/taxation_customs/dds2/eos/eori_home.jsp?Lang=en
    OrganizationID_Type_EO_ID: URIRef  # A type of identifier in the format of the invariant set of ISO646:1991 used in accordance with the EU Implementing Regulation 2018/574 to identify an economic operator.
    OrganizationID_Type_EU_VAT_IDENTIFICATION_NUMBER: URIRef  # An identifier used to identify companies for value added tax purposes in the European Union. Link: https://ec.europa.eu/taxation_customs/vies/faqvies.do#item_11
    OrganizationID_Type_FR_RCS: URIRef  # The RCS (Registre du commerce et des sociétés), otherwise known as the Greffe, is the registry for the company accounts and by-laws of all companies in France.
    OrganizationID_Type_FR_SIREN: URIRef  # The SIREN number, issued by Insee (the National Institute of Statistics and Economic Studies) is the unique identification number of each company. It is a number that allows each company to be identified by the administrations in France. The SIREN number also constitutes the first 9 digits of the SIRET number.
    OrganizationID_Type_IMO_COMPANY_NUMBER: URIRef  # IMO registers all vessels subject to the SOLAS convention. IMO also records the Owner, Operator, Manager and Group Beneficial Owner. For that purpose they also record the Companies acting in these roles using the IMO Company Number
    OrganizationID_Type_LEI: URIRef  # The Legal Entity Identifier (LEI) is a 20-character, alpha-numeric code based on the ISO 17442 standard developed by the International Organization for Standardization (ISO). It connects to key reference information that enables clear and unique identification of legal entities participating in financial transactions
    OrganizationID_Type_NL_KVK_NUMBER: URIRef  # When registering with the Netherlands Chamber of Commerce KVK, a business is listed in the Dutch Commercial Register or Handelsregister (HR) as it is called in the Netherlands. The businesses are then given a 8-digit KVK number. This number serves to prove an organisation is a registered business.
    OrganizationID_Type_NL_OIN_NUMBER: URIRef  # The Organization Identification Number (OIN) is a unique number assigned to organizations by Logius, the digital government service of the Netherlands Ministry of the Interior and Kingdom Relations, to identify, authenticate and/or authorise themselves in digital messaging within and with the government.
    OrganizationID_Type_NZ_GST_NUMBER: URIRef  # An identifier used to identify companies for goods and services tax purposes in New Zealand.
    OrganizationID_Type_NZ_IRD_NUMBER: URIRef  # An identifier used to identify companies for tax purposes in New Zealand.
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_1: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_10: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_2: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_3: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_4: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_5: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_6: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_7: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_8: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_ORG_FOR_INTERNAL_USE_9: (
        URIRef  # Identification used for internal mapping purposes.
    )
    OrganizationID_Type_PHYTOSANITARY_REGISTRATION_NUMBER: URIRef  # Within the European Union, the phytosanitary registration number identifies an organisation responsible for introducing, or moving plants, plant products and other objects, for which a phytosanitary certificate or a plant passport is required to comply with EU regulation. A phytosanitary registration number is not the same as a phytosanitary certificate number, which identifies the certificate issued to the organisation exporting items subject to phytosanitary processes.
    OrganizationID_Type_TIN: URIRef  # The taxpayer identification number (TIN) is an identifying number used for tax purposes in the United States and in other countries under the Common Reporting Standard. The unique identifier is assigned to the Account Holder by the tax administration in the Account Holder's jurisdiction of tax residence. It is a unique combination of letters and/or numbers used to identify an individual or entity for the purposes of administering the tax laws of that jurisdiction.  In some countries where the TIN is not used a national identification number, national identity number, or national insurance number is used by the governments of countries as a means of tracking their citizens, permanent residents, and temporary residents for the purposes of work, taxation, government benefits, health care, and other governmentally related functions.
    OrganizationID_Type_UK_CRN: URIRef  # A company registration number is a unique combination of numbers and, in some cases, letters. The company registration number (also known as the company number, registration number or simply abbreviated to CRN) is used to identify a company and verify that it is an entity registered with Companies House (the executive agency of the British Government reponsible for providing registered company information to the public).
    OrganizationID_Type_US_498_ID: URIRef  # A Service Provider Identification Number (SPIN) is a unique nine-digit number assigned to service providers by USAC when an FCC Form 498 is filed. This number is also known as the service provider's 498 ID.
    OrganizationID_Type_US_499_FILER_ID: URIRef  # The FCC Form 499 Filer Database is an identification system for all interstate telecommunications carriers, all interconnected VoIP providers, and certain other providers of interstate telecommunications.  The Universal Service Fund helps communities across the country afford telecommunications and advanced services.
    OrganizationID_Type_US_BEA_ID: URIRef  # The BEA foreign direct investment identification number is assigned to a new U.S. affiliate after their initial report has been accepted by the BEA. Filed by mail or facsimile, initial reports are due within 30 days of the end of the quarter in which the U.S. entity became foreign owned.
    OrganizationID_Type_US_CAGE: URIRef  # The Defense Logistics Agency (DLA) Commercial and Government Entity. A CAGE code is a five character alpha-numeric identifier assigned to entities located IN the United States and its territories
    OrganizationID_Type_US_CID: URIRef  # A company identification number, or CID, is given to a company when it is formed and the articles of organization or incorporation are approved by the U.S. Secretary of State. The CID is an important step when establishing a new company as it acts as a way to track important company information.
    OrganizationID_Type_US_CRD: URIRef  # Every stockbroker (registered representative) licensed to sell securities in the U.S. must have a CRD number, which is administered by the Financial Industry Regulatory Authority (FINRA).
    OrganizationID_Type_US_DEA: URIRef  # A DEA number (DEA Registration Number) is an identifier assigned to a health care provider (such as a physician, physician assistant, nurse practitioner, optometrist, podiatrist, dentist, or veterinarian) by the United States Drug Enforcement Administration allowing them to write prescriptions for controlled substances.
    OrganizationID_Type_US_DODAAC: URIRef  # Is a six position code that uniquely identifies a Department of Defense unit, activity, or organization that has the authority to requisition, contract for, receive, have custody of, issue, or ship DoD assets, or fund/pay bills for materials and/or services.
    OrganizationID_Type_US_EIN: URIRef  # The U.S. Employer Identification Number, also known as the Federal Employer Identification Number or the Federal Tax Identification Number, is a unique nine-digit number assigned by the Internal Revenue Service to business entities operating in the United States for the purposes of identification.
    OrganizationID_Type_US_EPA_ID: URIRef  # This number, issued either by the U. S. Environmental Protection Agency (U.S. EPA ID Number), or by DTSC (California ID Number), identifies each handler of hazardous waste on hazardous waste manifests and other paperwork.
    OrganizationID_Type_US_FCC_FRN: URIRef  # An FRN, or FCC registration number, is a 10-digit number that is assigned to a business or individual registering with the FCC.  The FCC will use the FRN to determine if all of a registrant's fees have been paid.
    OrganizationID_Type_US_FDIC: URIRef  # The FDIC Certificate ID is a unique number assigned to each depository institution by the Federal Deposit Insurance Corporation (FDIC).
    OrganizationID_Type_US_FHFA_ID: URIRef  # FHFA ID number is the number assigned to a member by FHFA and used by FHFA and the Banks to identify a particular member.
    OrganizationID_Type_US_FMC_ID: URIRef  # The Federal Maritime Commission (FMC) is a USA federal agency. The FMC is responsible for regulating USA ocean transportation to and from the USA. To buy or sell sea freight services to or from the USA, a company must be licensed or registered with the FMC.
    OrganizationID_Type_US_GIIN: URIRef  # GIIN is an abbreviation of Global Intermediary Identification Number. The FATCA Registration System approves foreign financial institutions (FFI), financial institution (FI) branches, direct reporting non-financial foreign entities (NFFE), sponsoring entities, sponsored entities, and sponsored subsidiary branches.
    OrganizationID_Type_US_LAB_ID: URIRef  # Code to identify CPSC-Accepted Testing Laboratories. Section 14(a)(3)(E) of the Consumer Product Safety (CPSC) Act, as amended, requires the Commission to maintain on its website an up-to-date list of entities that have been accredited to assess conformity with children's product safety rules.
    OrganizationID_Type_US_LIC: URIRef  # The assigned LIC identifies the registered company, not an individual product or device; it can be used across multiple product lines.
    OrganizationID_Type_US_MFG_ID: URIRef  # The United States Customs use the Manufacturer's Identification Number (MID) in the electronic data processing and monitoring of manufacturers. MID is an identifying reference number given to manufacturers that import products into the United States.
    OrganizationID_Type_US_MIC: URIRef  # Domestic boat manufacturers are required by U.S. federal law to obtain a unique Manufacturer's Identification Code (MIC). The same applies to domestic importers of foreign built vessels. This code must be incorporated as the first three characters of all hull identification numbers assigned to boats of their production.
    OrganizationID_Type_US_NPI: URIRef  # The National Provider Identifier (NPI) is a Health Insurance Portability and Accountability Act (HIPAA) Administrative Simplification Standard. The NPI is a unique identification number for covered health care providers. The NPI is a 10-position, intelligence-free numeric identifier (10-digit number).
    OrganizationID_Type_US_RN: URIRef  # RN stands for Registered Identification Number. It is a number issued by the FTC to U.S. businesses that manufacture, import, distribute, or sell products covered by the Textile, Wool, and Fur Acts. Businesses can use this number on product labels instead of the company name.
    OrganizationID_Type_US_RSSD_ID: URIRef  # The RSSD ID is a unique identifier assigned to financial institutions by the U.S. Federal Reserve.
    OrganizationID_Type_US_SCAC: URIRef  # The Standard Carrier Alpha Code (SCAC) is a unique two-to-four-letter code used to identify transportation companies. SCAC codes can be obtained from the National Motor Freight Traffic Association (NMFTA), located in Alexandria, VA.
    OrganizationID_Type_US_UEI: URIRef  # Uniquely identify entities registered in the U.S. government  System for Award Management (SAM)
    OrganizationRoleType: URIRef
    OrganizationRoleType_ACCEPTING_PARTY: URIRef  # Organization responsible for legally accepting goods or services at a physical location handled by a delivery party. The accepting process is part of a broader receiving process, focussed on preliminary checks of goods or services being delivered and occurs in the presence of the transport carrier. When physical goods are delivered, the accepting party will perform a visual check of the transport units (e.g., pallets) to identify any visual damages or defects, any discrepancies with the associated dispatch notice, and notify the transport carrier of any issues found, which can be challenged by the transport carrier if required. This process is defined by transport regulations, and if no issues are found, the goods are legally accepted, and transfer of ownership is completed (even if subject to further legal checks carried out by the checking party) and goods can proceed to checking and storing processes. An accepting party may be different to the party responsible for buying, ordering or paying for the goods or services. May also be different to the party responsible for physically receiving the goods on arrival or storing into inventory. For example, an accepting party may be a service provider to the buyer of goods, meaning goods may be accepted on behalf of the buyer, or prior to being taken over by the buyer.
    OrganizationRoleType_ACCOUNTS_DEPARTMENT: URIRef  # A business function or segment responsible for the preparation of financial statements, maintenance of general ledgers, payment of bills, preparation of customer bills, payroll, and other activities related to the management of finances within an organization. May also be known as a finance department.
    OrganizationRoleType_AGRICULTURAL_COOPERATIVE: URIRef  # An agricultural cooperative, also known as a farmers' co-op, is a cooperative in which farmers pool their resources in certain areas of activity.
    OrganizationRoleType_AIRPORT_OPERATOR: URIRef  # An organization or civil authority responsible for the oversight and management of all duties and processes within an airport, for example terminal operations, security, safety, communications, ground transportation and other activities related to the welfare of passengers, airlines, tenants and the general public.
    OrganizationRoleType_AREA_HEALTH_SERVICE: URIRef  # A grouping of entities, usually hospitals and associated healthcare service providers, which are defined as an Area Health Service and based on distinct geographic areas as defined by the region or country. May also be known as a regional health organization.
    OrganizationRoleType_ARRIVING_GOODS_PARTY: URIRef  # Organization responsible for physically receiving  goods arriving at a physical location, where goods may be temporarily stored ahead of being legally accepted and formally checked. The arriving goods process, is the first part of a broader receiving process, focussed primarily on handling goods so they are prepared and ready for the subsequent accepting and checking processes. The arriving goods party may be different to an accepting or checking party as processes to legally accept a delivery, or to confirm receipt to inventory are not necessarily included.
    OrganizationRoleType_BILL_OF_LADING_RECIPIENT: URIRef  # Organization that needs to receive the Bill of Lading document (abbreviated as BOL or B/L). A BOL is used by many actors in the transport and supply chain sector to serve three main functions: as a conclusive receipt to acknowledge that goods have been physically loaded to a transport carrier; as evidence of the terms for the contract of carriage; and as a document of title, which may be used to claim ownership of the goods described on the BOL. Some common examples of BOL recipients include the shipper handing over goods to the transport carrier at the point of origin, or the buyer of goods who can use the BOL to claim release of the goods from the transport carrier at the destination.
    OrganizationRoleType_BILL_TO: URIRef  # Organisation that needs to receive the Bill of Lading document (abbreviated as BOL or B/L). A BOL is used by many actors in the transport and supply chain sector to serve three main functions: as a conclusive receipt to acknowledge that goods have been physically loaded to a transport carrier; as evidence of the terms for the contract of carriage; and as a document of title, which may be used to claim ownership of the goods described on the BOL. Some common examples of BOL recipients include the shipper handing over goods to the transport carrier at the point of origin, or the buyer of goods who can use the BOL to claim release of the goods from the transport carrier at the destination.
    OrganizationRoleType_BRANCH: URIRef  # An organization segment, that operates in different locations or jurisdictions than its parent organization. A branch is an extension of an existing company and does not constitute a separate legal entity, unlike a subsidiary or sub-organization.
    OrganizationRoleType_BRAND_OWNER: URIRef  # An organization who provides any commodity under a registered brand name or label. A brand owner may sell their commodities directly to consumers, retailers or marketplaces; or they may simply provide the rights to their brand name, for example, for manufacturers to produce goods with their brand name, as contracted with a retailer.
    OrganizationRoleType_BREEDER: URIRef  # An organization which breeds animals, including aquatic vertebrates such as fish, according to their genealogy, characteristics, and offspring. A breeder is responsible for facilitating reproduction and birthing processes for a specific species. Includes care and rearing activities, but does not include cross-breeding for new species.
    OrganizationRoleType_BROKER_AGENT: URIRef  # A broker or agent acts as an intermediary between its clients and other actors in cases where the client cannot or will not interact directly with those other actors. The services of brokers and agents vary widely. Examples include buying/selling products or services, representation of their clients towards authorities, agencies or other actors in a specific geography etc.
    OrganizationRoleType_BUYER: URIRef  # The organization purchasing goods or services, from a seller. May be different to the party responsible for ordering, receiving or accepting the goods or services.
    OrganizationRoleType_BUYERS_AGENT_REPRESENTATIVE: URIRef  # Third party who arranged the purchase of merchandise on behalf of the actual buyer.
    OrganizationRoleType_BUYING_DEPARTMENT: URIRef  # A business function or segment responsible for acquiring goods and services for a business to operate, including the monitoring of supply chains and negotiating contracts with vendors. May also be known as a procurement or purchasing department.
    OrganizationRoleType_CARRIER: URIRef  # A company, which physically transports goods from one place to another.
    OrganizationRoleType_CENTRAL_PAYMENT_SERVICE: URIRef  # Master of the conveyance. An organization providing central (or consolidated payment) services.
    OrganizationRoleType_CHECKING_PARTY: URIRef  # Organization designated on behalf of a transport carrier, an agent or goods owner who is responsible for the detailed checks of goods being sent or received. For goods being sent (outbound deliveries), the checking process is part of a broader sending process and establishes the actual figures of a shipment or consignment, checking product codes, product condition, quantities, weight, volume and/or cubic measurements of goods or containers which are included in a transport or trade contract and on which charges will be based. For goods being received (inbound deliveries), the checking process is part of a broader receiving process, focussed on detailed verification of what has been delivered and accepted, to confirm the physical contents of the transport units matches the delivery advice. If there are any issues found, sometimes known as 'hidden vices', the checking party is responsible for notifying the relevant parties, within a designated time frame from the receipt date of the shipment. Unlike the preliminary checks carried out by the accepting party, the checking process occurs after the transport carrier has left the premises. A checking party may be different to the party responsible for buying, ordering or paying for the goods or services. May also be different to the party responsible for physically receiving the goods on arrival or storing into inventory. For example, a checking party may be a service provider to the buyer of goods, meaning goods may be checked on behalf of the buyer, or prior to being stored in inventory.
    OrganizationRoleType_CHECK_ORDER: URIRef  # Organization to which the check will be ordered, when different from the beneficiary.
    OrganizationRoleType_CLINICAL_TRIAL_SPONSOR: URIRef  # A person, company, institution, group, or organization that oversees or pays for a clinical trial and collects and analyses the data.
    OrganizationRoleType_COMPLIANCE_AUTHORITY_OR_AGENCY: URIRef  # An organization, which is generally part of a government, that is responsible for ensuring compliance of products or services with the requirements specified in laws or regulations. These authorities may certify one or more conformance assessment body(ies) to perform the activities required to check compliance.
    OrganizationRoleType_CONFORMITY_ASSESSMENT_BODY: URIRef  # An organization that performs third-party conformity assessment activities, including testing, certification and inspection.
    OrganizationRoleType_CONSIGNEE: URIRef  # Organization who receives goods from another party. The consignee may take title/ownership of the goods upon delivery or they may have taken ownership earlier in the process based on international commercial terms (known as Incoterms) agreed between the buyer and seller of the goods. The party identified as the consignee is an important element in cross-border transportation procedures, such as customs clearance and payment of taxes, for example.
    OrganizationRoleType_CONSIGNOR: URIRef  # Organization who dispatches goods to another party. The consignor will keep the title/ownership of the goods being transported and is legally liable until the goods are transferred to or paid for by the consignee or the final party.
    OrganizationRoleType_CONSOLIDATOR: URIRef  # An organization or department that combines transport units into larger consignments for shipping. A consolidator is different to a packer who packs physical goods for transportation and sale. Is also different to a repacker, who combines various goods into a single pack for sale or shipping.
    OrganizationRoleType_CONSUMER: URIRef  # The end user of a product or a service.
    OrganizationRoleType_CORPORATE_IDENTITY: URIRef  # An organization that represents the identity of a commercial organization, commonly known as a holding or parent company, and links a number of other organizations or affiliated sub-organizations.
    OrganizationRoleType_COUNTRY_ORGANIZATION: URIRef  # An organization that operates and/or is responsible for processes, activities and operations within a specific country (or a small grouping of adjacent countries), under the structure of a multinational or global organization. A country organization may be a separate legal entity and considered as a sub-organization or subsidiary of a parent organization.
    OrganizationRoleType_CUSTOMS: URIRef  # Identification of customs authority relevant to the transaction or shipment.
    OrganizationRoleType_CUSTOMS_AUTHORITY: URIRef  # An organization, typically a government authority or agency commonly known as 'customs', who is responsible for the administration and enforcement of jurisdictional customs laws and regulations of a country or territory, for example collecting taxes on goods entering the country and preventing illicit goods from entering a country.
    OrganizationRoleType_CUSTOMS_BROKER: URIRef  # An organization providing services for the preparation of documents and/or electronic submissions, the calculation of taxes, duties and excises on behalf of the client, and facilitating communication between the importer/exporter and governmental authorities.
    OrganizationRoleType_CUTTER: (
        URIRef  # One engaged in carving meat (In EANCOM as Meat Cutter).
    )
    OrganizationRoleType_DATA_CONSUMER: URIRef  # The organization receiving data from other organizations in any format and through any type of data sharing or transfer mechanism.
    OrganizationRoleType_DATA_PROVIDER: URIRef  # The organization providing data to other organizations in any format and through any type of data sharing or transfer mechanism.
    OrganizationRoleType_DECLARANTS_AGENT_REPRESENTATIVE: URIRef  # Any natural or legal person who makes a declaration to an official body on behalf of another natural or legal person, where legally permitted (CCC).
    OrganizationRoleType_DELIVERY_PARTY: (
        URIRef  # Organization to which goods are delivered.
    )
    OrganizationRoleType_DELIVERY_RECIPIENT_PARTY: URIRef  # Organization responsible for the physical location where goods or services are delivered by a transport carrier, and/or taken over by the buyer. The delivery recipient party may be different to the party responsible for buying, ordering,  accepting or paying for the goods or services; may also be different to the party responsible for receiving consigned shipments between carriers. For example, a delivery recipient party may be a service provider to the buyer of goods, liaising with freight forwarders to confirm transportation of goods.
    OrganizationRoleType_DESIGNER: URIRef  # An organization who designs.
    OrganizationRoleType_DESPATCH_PARTY: (
        URIRef  # Organization where goods are collected or taken over by the carrier.
    )
    OrganizationRoleType_DISPATCH_PARTY: URIRef  # Organization responsible for the physical location where goods may be collected or taken over by the transport carrier for dispatch. The dispatch party may be different to the party responsible for selling or receiving payment for the goods or services; and may also be different to the party responsible for consigning shipments between carriers. For example, a dispatch party may be a service provider to the seller of goods, liaising with a freight forwarder to arrange transportation of the goods.
    OrganizationRoleType_DISTRIBUTION_MANAGEMENT_ENTITY_PROVIDER: URIRef  # Organization providing a Distribution Management Entity (DME) system that is used to manage the distribution and disposition of clinical supplies. In many cases, this is the interactive technology IRT system, portal, a set of tools or different databases used to share information during a clinical trial.
    OrganizationRoleType_DISTRIBUTOR: URIRef  # An organization in the distribution channel or supply chain that is an intermediary between a producer or manufacturer of goods and a downstream entity such as a retailer or reseller, responsible for facilitating services within distribution processes.
    OrganizationRoleType_DOCK_DOOR: URIRef  # A door or collection of doors where trucks or rail cars are loaded (shipping) or unloaded (receiving). Used to load or unload products for logistics.
    OrganizationRoleType_EMERGENCY_DEPARTMENT: URIRef  # A department within a hospital organization that is responsible for providing emergency care to patients who require urgent medical attention.
    OrganizationRoleType_EMPTY_EQUIPMENT_DISPATCH_PARTY: URIRef  # Organization from whose premises empty equipment will be or has been dispatched.
    OrganizationRoleType_EMPTY_EQUIPMENT_RETURN_PARTY: URIRef  # Organization from whose premises empty equipment will be or has been returned.
    OrganizationRoleType_EQUIPMENT_OWNER: (
        URIRef  # Owner of equipment (e.g.,container, etc.).
    )
    OrganizationRoleType_EXPORTER: URIRef  # An organization that sends goods or services to another country for sale. An exporter, or a customs clearing agent or other authorised person acting on behalf of the exporter, is responsible for making an export declaration. This may include a manufacturer, seller or other person. Within a Customs union, consignor may have the same meaning as exporter.
    OrganizationRoleType_E_TAILER: URIRef  # A retailer offering a varied selection of goods or services through an online store (i.e., via electronic transactions on the internet) for purchase by consumers, without the presence of a physical store.
    OrganizationRoleType_FACILITIES_MAINTENANCE_DEPARTMENT: URIRef  # A business function or segment responsible for the regular upkeep and maintenance of equipment, machinery, furnishings as well as building structures and grounds of a physical location. May include, but  not limited to, tasks such as cleaning, servicing, repairing, gardening, safety conformance checks and certifications etc.
    OrganizationRoleType_FACTOR: URIRef  # An organization that purchases financial receiving instruments e.g. invoices
    OrganizationRoleType_FARM_OPERATOR: URIRef  # An organization who tends to plants and/or animals for the production of foodstuffs for eventual consumption (e.g., vegetables, meat or dairy), or livestock for labour or leisure purposes  (e.g., work horse or pet).
    OrganizationRoleType_FATTENER: URIRef  # The organization which fattens the animal.
    OrganizationRoleType_FISHING_OPERATOR: URIRef  # Organization who collects non-domesticated creatures from bodies of water for eventual consumption.
    OrganizationRoleType_FOODSERVICE_DISTRIBUTOR: URIRef  # Organization that provides food and non-food products to restaurants, cafeterias, industrial caterers, hospitals, schools/colleges/universities, nursing homes, and anywhere food is served away from the home.
    OrganizationRoleType_FOODSERVICE_OPERATOR: URIRef  # An organization which offers food and beverages to the public, either for purchase or as part of a service relationship with another party, for example for a private function.
    OrganizationRoleType_FREIGHT_FORWARDER: URIRef  # An organization that organizes shipments for individuals or other organizations to transport goods from the collection of goods at a point of origin to a specified destination. Freight forwarders typically contract with transportation carriers to move goods.
    OrganizationRoleType_GOODS_OWNER: URIRef  # The organization which owns the goods.
    OrganizationRoleType_GOVERNMENT_AGENCY: URIRef  # A permanent or semi-permanent organization that may be established by a national or state government within a federal system, that is responsible for the oversight and administration of specific functions. For example the UK's Driver and Vehicle Licensing Agency (DVLA).
    OrganizationRoleType_GOVERNMENT_DEPARTMENT_OR_MINISTRY: URIRef  # An organization or department within a government body that manages a specific sector of public administration and may oversee other government agencies and organizations as part of a political portfolio. For example, the UK's Department for Transport (DfT), oversees the UK's Driver and Vehicle Licensing Agency (DVLA). Usually led by a high-ranking government official or politician such as a minister, secretary or commissioner and staffed with members of a non-political civil service to manage operations.
    OrganizationRoleType_GROWER: URIRef  # An organization which is responsible for the growth and/or production of plants and crops such as fruit and vegetable produce, ornamental plants and trees, medicinal or cooking herbs etc. This organization may or may not be a producer or packer.
    OrganizationRoleType_HARVESTER: URIRef  # Organization who collects ready for harvest foodstuffs from farms for utilization or consumption by subsequent parties.
    OrganizationRoleType_HEALTHCARE_PROVIDER: URIRef  # An organization providing healthcare services for primary care, nursing care and speciality care and/or treatments. Includes specialized providers such as surgeons, midwives, therapists, dentists for example.
    OrganizationRoleType_HOSPITAL_ORGANIZATION: URIRef  # A healthcare organization responsible for a hospital facility providing patient treatment with specialized medical and nursing staff, medical equipment and inpatient care facilities.
    OrganizationRoleType_HOSPITAL_PHARMACY_OPERATOR: URIRef  # An organization and individual legal entity engaged in the activities of ordering and dispensing medications for the treatment of patients within a hospital facility, often at the direction of or by working directly with physicians, nurses or other specialized healthcare providers. Differs to a retail pharmacy operator in a retail pharmacy, as hospital pharmacists require specific clinical training and qualifications to handle specialist activities such as formulating patient specific doses or medications, preparing intravenous (IV) compounds, for example.
    OrganizationRoleType_IMPORTER: URIRef  # Organization who makes - or on whose behalf a Customs clearing agent or other authorized person makes - an import declaration. This may include a person who has possession of the goods or to whom the goods are consigned.
    OrganizationRoleType_INFORMATION_PROVIDER: (
        URIRef  # The organization providing the information contained in the document.
    )
    OrganizationRoleType_INSURER: (
        URIRef  # A person or company offering insurance policies for premiums.
    )
    OrganizationRoleType_INTERMEDIARY_BANK: URIRef  # A financial institution between the ordered bank and the beneficiary's bank.
    OrganizationRoleType_INTERMEDIARY_BANK_1: URIRef  # A financial institution between the ordered bank and the beneficiary's bank.
    OrganizationRoleType_INTERMEDIARY_BANK_2: URIRef  # A financial institution between the ordered bank and the beneficiary's bank.
    OrganizationRoleType_INVENTORY_CONTROLLER: URIRef  # To specifically identify the organisation in charge of inventory control.
    OrganizationRoleType_INVENTORY_REPORTING_PARTY: (
        URIRef  # Organization reporting inventory information.
    )
    OrganizationRoleType_INVOICEE: URIRef  # The organization to whom an invoice is issued, which may be different to the organization to whom the invoice is sent to for processing e.g., BILL_TO and INVOICE_MUST_BE_SENT_TO. May also be different to the party ordering, accepting, buying, or initiating payment for the goods or services.
    OrganizationRoleType_ISSUER_OF_INVOICE: URIRef  # The organization issuing an invoice. May be different to the party selling, dispatching, or receiving payment for the goods or services.
    OrganizationRoleType_LOGISTICS_SERVICE_PROVIDER: URIRef  # An umbrella term for an organization, which provides a combination of different logistics services for another organization, such as transportation, storage and handling, freight forwarding, packing and repacking etc. Commonly known as a third-party logistics service provider (3PL).
    OrganizationRoleType_MANUFACTURER_OF_FINISHED_GOODS: URIRef  # An organization that has final responsibility for producing the finished goods, components or finished goods from raw materials and/or by assembling other components or finished goods. Finished goods are considered complete and ready for use. Includes third-party manufacturers, known as contract manufacturers, who handle the full production operations on behalf of another organization.
    OrganizationRoleType_MANUFACTURER_OF_GOODS: (
        URIRef  # Organization who manufactures the goods.
    )
    OrganizationRoleType_MANUFACTURER_OF_UNFINISHED_GOODS: URIRef  # An organization that produces semi-finished goods, components or semi-finished goods from raw materials and/or by assembling other components or semi-finished goods. Semi-finished goods are not consumer-ready. Includes third-party manufacturers, known as contract manufacturers, who handle the full production operations on behalf of another organization.
    OrganizationRoleType_MARKETING_DEPARTMENT: URIRef  # A business function or segment responsible for promoting an organization's brand, products and/or services, through the planning, creating and monitoring of marketing activities such as for brand management, promotional material and campaigns , and website content and search optimisations.
    OrganizationRoleType_MARKETPLACE_OPERATOR: URIRef  # Organization which provides an online platform specifically for independent sellers to offer a varied selection of products for purchase by consumers. May also operate as an e-tailer, if the marketplace operator's own brand(s) are also sold online.
    OrganizationRoleType_MARK_FOR: URIRef  # The ultimate destination of a unit load or transport package of goods where the Ship-To is a different location.
    OrganizationRoleType_MENTAL_HEALTH_SERVICE: URIRef  # An organization providing mental health treatment and support services.
    OrganizationRoleType_MESSAGE_FROM: (
        URIRef  # Organization where the message comes from.
    )
    OrganizationRoleType_MESSAGE_RECIPIENT: (
        URIRef  # Organization receiving the message.
    )
    OrganizationRoleType_MINCER: (
        URIRef  # One engaged in the cutting or chopping of meat into very small pieces
    )
    OrganizationRoleType_OPERATING_DIVISION: URIRef  # An operational department or business segment of an organization, which may have multiple days and times of operation, which differs to other departments or the main organization.
    OrganizationRoleType_OPERATOR: URIRef  # An organization who operates a business establishment, or has specific capabilities to operate equipment, machinery or devices.
    OrganizationRoleType_ORDERING_PARTY: URIRef  # Organization responsible for ordering goods or services. The ordering party may be different to the party responsible for buying, accepting, receiving or paying for the goods or services; may also be different to the delivery party responsible receiving goods at a physical location. For example, an ordering party may be a service provider to the buyer of goods, meaning the goods are ordered on behalf of the buyer.
    OrganizationRoleType_OWNER_OF_EQUIPMENT: URIRef  # Organization who owns equipment.
    OrganizationRoleType_OWNER_OF_MEANS_OF_TRANSPORT: URIRef  # An organization who owns the means of transport, which may be leased or loaned for use by a transportation carrier or service provider.
    OrganizationRoleType_PACKER: URIRef  # An organization or department that packs physical goods for transportation and sale. A packer is different to a consolidator who combines transport units into larger consignments for shipping, and is also different to a repacker, who combines various goods into a single pack for sale or shipping.
    OrganizationRoleType_PARTY_DECLARING_THE_VALUE_ADDED_TAX: URIRef  # A code to identify the organization who is responsible for declaring the Value Added Tax (VAT) on the sale of goods or services.
    OrganizationRoleType_PARTY_FOR_WHOM_ITEM_IS_ULTIMATELY_INTENDED: (
        URIRef  # Party for whom item is ultimately intended.
    )
    OrganizationRoleType_PARTY_RECEIVING_PRIVATE_DATA: URIRef  # The organization who is allowed access to master data information by the data owner when the data is viewed as private.
    OrganizationRoleType_PARTY_RECOVERING_THE_VALUE_ADDED_TAX: URIRef  # A code to identify the organization who is eligible to recover the Value Added Tax (VAT) on the sale of goods or services.
    OrganizationRoleType_PARTY_TO_RECEIVE_ALL_DOCUMENTS: (
        URIRef  # An organization which is named to be the recipient of all documents.
    )
    OrganizationRoleType_PARTY_TO_RECEIVE_COMMERCIAL_INVOICE: URIRef  # Organization that needs to receive the commercial invoice. A commercial invoice is issued by a seller to the buyer of the goods or services and is often used as part of a customs declaration for foreign trade. It is needed for a wide range of services provided by actors in supply chain, transport and logistics processes, who are not involved in the buying and selling transaction covered by regular invoices.
    OrganizationRoleType_PARTY_TO_RECEIVE_ELECTRONIC_MEMO_OF_INVOICE: URIRef  # Organization that needs to receive notification for an invoice being issued, which may or may not be the same as the party identified as the invoice recipient, processor, or payer. For example, an external certification body, or a bank providing loans.
    OrganizationRoleType_PARTY_TO_RECEIVE_FREIGHT_BILL: (
        URIRef  # Organization to whom the freight bill should be sent.
    )
    OrganizationRoleType_PARTY_TO_RECEIVE_REFUND: (
        URIRef  # Organization to whom a refund is given.
    )
    OrganizationRoleType_PAYEE: URIRef  # The organization receiving payment, and may be different to the party who sends the invoice, goods or services related to the payment.
    OrganizationRoleType_PAYER: URIRef  # The organization initiating payment, and may be different to the party who receives the invoice, goods or services related to the payment.
    OrganizationRoleType_PHARMACY_OPERATOR: URIRef  # Organization engaged in the activities of ordering and dispensing medications for members of the public, often at the direction of physicians.
    OrganizationRoleType_PORT_OPERATOR: URIRef  # An organization or civil authority responsible for the oversight and management of all duties and processes within a seaport or inland port, for example terminal operations, security, safety, communications, in-port transportation, vessel traffic services and other activities related to the welfare of passengers, shipping lines, tenants and the general public.
    OrganizationRoleType_PRICE_LOCATION_PARTY: URIRef  # An organization to which a price for a product is applicable. Within the context of GDSN Price Synchronization, it is also known as the 'Price Location' which is a GLN.
    OrganizationRoleType_PROXY: URIRef  # A company that is selected by the Brand Owner to maintain their baseline attributes and Administrative Records in the GDSN.
    OrganizationRoleType_PURCHASE_ORDER_RECEIVER: URIRef  # The organization that receives the purchase order for the goods or services.
    OrganizationRoleType_RECALL_RECIPIENT: URIRef  # Organisation/Location/Individual receiving Recall notifications via local Recall Service.
    OrganizationRoleType_RECALL_SPONSOR: (
        URIRef  # Organisation sending Recall notifications via local Recall Service.
    )
    OrganizationRoleType_REGIONAL_ORGANIZATION: URIRef  # An organization that operates and/or is responsible for processes, activities and operations within a specific geographical region and across a number of different countries, under the structure of a multinational or global organization. A regional organization may be a separate legal entity and considered as a sub-organization or subsidiary of a parent organization.
    OrganizationRoleType_REGISTERED_AGENT: URIRef  # The organization having legal responsibility for the product in the target market for example a company to which market authorization has been issued.
    OrganizationRoleType_REMIT_TO: URIRef  # Organization to whom funds are directed for payment of a commercial invoice.
    OrganizationRoleType_REPACKER: URIRef  # Organization or department responsible for repacking goods for resale or for transportation purposes, without modifying the repacked products in any way. A repacker is different to packer who packs physical goods for transportation and sale; and is also different to a consolidator who combines transport units into larger consignments for shipping.
    OrganizationRoleType_RETAILER: URIRef  # An organization who makes a varied selection of products available for purchase by consumers, either through operating physical or online stores.
    OrganizationRoleType_RETAIL_PHARMACY_OPERATOR: URIRef  # An organization or individual legal entity engaged in the activities of ordering and dispensing medications for members of the public within a retail pharmacy, often at the direction of physicians. A retail pharmacy operator differs from a hospital pharmacy operator as they usually interact with the public to provide advice about their prescription, instead of working directly with healthcare specialists such as nurses and doctors to ensure the right medications are prescribed.
    OrganizationRoleType_SALES_DEPARTMENT: URIRef  # A business function or segment responsible for selling goods and services to meet customer needs. Includes activities to increase profitability, forecasting and meeting sales targets, building and maintaining customer relationships, encouraging repeat purchases and brand loyalty.
    OrganizationRoleType_SELLER: URIRef  # The organization selling goods or services, to a buyer. May be different to the party responsible for dispatching the goods or services.
    OrganizationRoleType_SERVICE_PROVIDER: URIRef  # An organization providing services to another organization or directly to consumers. Some examples include (but are not limited to) consulting, advertising, legal, communications, transport, technology or processing services.
    OrganizationRoleType_SHIPPER: URIRef  # The party that initiates a contract for carriage with, and arranges for delivery of the goods to, a carrier or transport intermediary for transportation.
    OrganizationRoleType_SHIP_FROM: (
        URIRef  # Organization from where goods will be or have been shipped.
    )
    OrganizationRoleType_SHIP_FROM_PARTY: URIRef  # An organization which sends physical goods and invoices, and is often the same party as the consignor. However in some cases, a consignor may designate a third party to manage the facility where the goods are shipped from, which is different to the dispatch party responsible for the facility where the goods are dispatched from.
    OrganizationRoleType_SHIP_TO: (
        URIRef  # Organization which receives goods and invoices.
    )
    OrganizationRoleType_SHIP_TO_PARTY: URIRef  # An organization which receives physical goods and invoices, and is often the same party as the consignee. However in some cases, a consignee may designate a third party to manage the facility where the goods are shipped to, which is different to the delivery recipient party responsible for the facility where goods are received.
    OrganizationRoleType_SLAUGHTERER: URIRef  # An organization which is responsible for slaughtering livestock and preparing carcasses for further processing, including specialized tasks such as the removal of organs, hides and/or specific premium cuts.
    OrganizationRoleType_STORAGE_AND_HANDLING: URIRef  # The movement, protection, storage of products throughout manufacturing, warehousing and distribution
    OrganizationRoleType_STORAGE_AND_HANDLING_PARTY: URIRef  # An organization or department responsible for the storage and handling of goods within a facility; may be included with other services offered by a logistics service provider or a leased warehouse space for example and is often a third party, that is external to the parties directly employed by the facility.
    OrganizationRoleType_SUBSTITUTE_SUPPLIER: URIRef  # Organization which may be in a position to supply products or services should the main usual supplier be unable to do so.
    OrganizationRoleType_SUPPLIER: (
        URIRef  # An organization that provides goods or services.
    )
    OrganizationRoleType_SUPPLY_CHAIN: URIRef  # A business function or segment responsible for the end-to-end process of manufacturing and trading commercial goods, with a broad scope covering procurement processes as well as traditional logistics processes involving warehousing and transportation
    OrganizationRoleType_TECHNICAL_SUPPORT_DEPARTMENT: URIRef  # A business function or segment responsible for providing assistance and support for their organization's technical equipment and/or system infrastructure, for example with hardware such as computers, mobile phones and servers or software issues and configurations. Technical support may be provided as a service for internal staff or for external customers.
    OrganizationRoleType_TRADER: URIRef  # An organisation that engages in the buying and selling of financial assets in any financial market, either for themself or on behalf of another person or institution.
    OrganizationRoleType_TRADER_FINANCIAL: URIRef  # An organization that engages in the buying and selling of financial assets in any financial market, either for themselves or on behalf of another person or institution.
    OrganizationRoleType_TRADER_GOODS: URIRef  # An organization that engages in the buying and selling of tangible goods such as raw materials and fresh produce. Goods may be traded in any market, either for themselves or on behalf of another party.
    OrganizationRoleType_TRANSPORTATION_CARRIER: URIRef  # An organization that undertakes or arranges the physical transportation of goods from one identified place to another. A transportation carrier is usually contracted by a freight forwarder to move goods within a regular route, for a set rate.
    OrganizationRoleType_WAREHOUSE_KEEPER: URIRef  # Organization who is responsible for a warehouse location and the goods that are kept on-site within the facility.
    OrganizationRoleType_WHOLESALER: URIRef  # An organization that sells products, often in large quantities, to be retailed by others.
    OrganizationStatusHistory: URIRef  # Over the lifetime of an organisation, it may go through periods of being active and inactive. gs1:OrganizationStatusHistory allows changes in status to be communicated in advance and tracked over time.
    PackagingDetails: URIRef  # Details on packaging for a product for example packaging type (bottle), materials, features, recycling, etc..
    PackagingFeatureCode: URIRef
    PackagingFeatureCode_BASE: (
        URIRef  # A general term applied to the support or pedestal of an object.
    )
    PackagingFeatureCode_BEAM: URIRef  # Long sturdy piece of squared timber or metal used in house-building etc.
    PackagingFeatureCode_BUNG_SEAL: URIRef  # A bung is an apparatus used to seal a container, such as a bottle, barrel or tubes. A bung is partially inserted inside the container to act as a seal. The most common every-day example of a bung is the stopper of a wine bottle.
    PackagingFeatureCode_CAP: (
        URIRef  # A cap that seals a bottle or other form of packaging.
    )
    PackagingFeatureCode_CARRIER: URIRef  # A device of various types attached to or hung from trolleys to support the load.
    PackagingFeatureCode_CONSUMPTION_UTENSIL: URIRef  # An item which allows the user to extract and/or consume the content of a container.
    PackagingFeatureCode_CORE: URIRef  # A tubular shape around which flexible material such as plastic film or paper are wound for purposes of transport and handling.
    PackagingFeatureCode_CREEL: URIRef  # A creel is a device for holding the required number of roving spools or other supply packages of reinforcement fibers for Fiber Reinforced Plastics manufacturing. This device holds the rovings in the desired position for unwinding in continuous processes like Pultrusion and Filament Winding.
    PackagingFeatureCode_EDGE_PROTECTION: URIRef  # A right-angle piece placed over the outermost perimeter edges of a container to distribute pressure and prevent collapse or cutting from banding, strapping, or handling.
    PackagingFeatureCode_HANDLE: URIRef  # A grip attached to an object for using or moving the object, usually with the hands.
    PackagingFeatureCode_INNER_CONTAINER: URIRef  # Inner Container
    PackagingFeatureCode_INTERNAL_DIVIDER: URIRef  # An internal divider is an object, either flat or custom-shaped, used to separate the content of a container or to prevent the content from mixing.
    PackagingFeatureCode_LABEL: URIRef  # A label is a piece of paper, polymer, cloth, metal, or other material affixed to a container or article (or printed directly upon it), which usually carries information about the article to.which it has been attached.
    PackagingFeatureCode_LID: URIRef  # In packaging, the top or bottom of a container, usually the part that closes the opening; may also be known as cap, over, or top
    PackagingFeatureCode_LINER: URIRef  # An internal chamber within a container which separates the content of the container from the walls. Inner liners provide additional isolation and protection to the content of a container. Sometimes coatings of certain materials may be applied as an alternative to inner liners.
    PackagingFeatureCode_LUG: URIRef  # A small indentation or raised portion on the surface of a bottle, provided as an indexing means for operations such as multi-pass decoration or labeling.
    PackagingFeatureCode_NESTING_EDGE: URIRef  # Edges which allow items of the same size to be partially stacked within one another in any direction thus reducing the space required in order to stack them.
    PackagingFeatureCode_PEG: URIRef  # A fastener which allows a product to be hanged.
    PackagingFeatureCode_PULL_OFF_TAB: URIRef  # A flexible cover which can be easily removed in order to open a container.
    PackagingFeatureCode_RING_HOLDER: (
        URIRef  # A hollow circular band of material wound around itself.
    )
    PackagingFeatureCode_RIVET: URIRef  # A permanent fastener which consists of a cylindrical shaft with a head on one end and tail which is deformed to fixate the rivet in place.
    PackagingFeatureCode_SLEEVE: URIRef  # A tubular form, open at both ends, that is slipped over an item or package.
    PackagingFeatureCode_SPOUT: URIRef  # A spout is a protruding edge which allows the lifting and pouring of liquids contained within a container.
    PackagingFeatureCode_TAG: URIRef  # A hanging card made of any material which is used to identify or provide additional information of a product.
    PackagingFeatureCode_WICKER_OUTER_CONTAINER: URIRef  # An outer container made of wicker which is fitted to the bottle usually a little less than half way up from the bottom of the bottle and is used to hold, hang or support the bottle.
    PackagingFeatureCode_WRAP: URIRef  # A layer of any material which completely enclose a product. A wrap can have many purposes, from providing additional protection to an item to serving as a gift-wrap.
    PackagingFunctionCode: URIRef
    PackagingFunctionCode_ANTISEPTIC: URIRef  # The process by which a sterile (aseptic) product (typically food or pharmaceutical) is packaged in a sterile container in a way which maintains sterility.
    PackagingFunctionCode_ANTI_TAMPERING: URIRef  # A methodology used to hinder, or deter unauthorized access to a device.
    PackagingFunctionCode_COATED: URIRef  # Covered with a material (paraffin, wax) that protects the product or packaging.
    PackagingFunctionCode_COMPRESSED: (
        URIRef  # Content has been pressed together to the maximum possible way.
    )
    PackagingFunctionCode_DISPENSER: (
        URIRef  # A device or mechanism to supply or extract contents.
    )
    PackagingFunctionCode_GIFT_WRAPPED: URIRef  # Packaging is wrapped in a decorative way for the purposes of the consumer giving it as a gift.
    PackagingFunctionCode_ISOTHERMIC: URIRef  # Thermal carry container designed for the carriage of temperature controlled goods such as vaccines, pharmaceuticals, and medicines.
    PackagingFunctionCode_MODIFIED_ATMOSPHERE: URIRef  # The practice of modifying the composition of the internal atmosphere of a package, (commonly food packages, and drugs) in order to improve the shelf life.
    PackagingFunctionCode_OXYGEN_INFUSED: (
        URIRef  # A barrier packaging material for an infusion solution, i.e., oxygen.
    )
    PackagingFunctionCode_PEEL_OFF: URIRef  # A section of the packaging can be detached with ease in order to have access to the content or product, e.g. peel-off Lids used for packing Milk, Coffee and Cacao Powder.
    PackagingFunctionCode_PINPACK: (
        URIRef  # The package is equipped to be hung up on a hook.
    )
    PackagingFunctionCode_PROTECTED: URIRef  # Functionality to keep from being damaged, attacked, stolen, or injured; guard.
    PackagingFunctionCode_REINFORCED: URIRef  # A component is added to a container for a particular application to lend additional support under severe applications.
    PackagingFunctionCode_SIFT_PROOF: URIRef  # Packaging is designed to prevent leaking of the content specially when it is on powdered or liquid state.
    PackagingFunctionCode_TAMPER_EVIDENT: URIRef  # The packaging is designed to show when there has been some interference with the original sealing or configuration of the packaging.
    PackagingFunctionCode_WATER_RESISTANT: URIRef  # Coated with materials that make the packaging impervious to the effects of water.
    PackagingMarkedDietAllergenCode: URIRef
    PackagingMarkedDietAllergenCode_APPROVED_BY_ASTHMA_AND_ALLERGY_ASSOC: (
        URIRef  # Definitions made by the asthma and allergist association.
    )
    PackagingMarkedDietAllergenCode_APPROVED_FOR_TUBE_FEEDING: URIRef  # The item is physically marked that it is approved for tube feeding by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_BIOLOGICAL: URIRef  # Indicates the product has been marked as a biological item which indicates a food product that was produced with the use of feed or fertilizer of plant or animal origin, without employment of chemically formulated fertilizers, growth stimulants, antibiotics or pesticides.
    PackagingMarkedDietAllergenCode_CALORIES_PER_PORTION: URIRef  # Indicates the product has a marking with the calories per portion contained in the product.
    PackagingMarkedDietAllergenCode_CONTAINS_LATEX: (
        URIRef  # The item is physically marked as containing Latex (rubber).
    )
    PackagingMarkedDietAllergenCode_CONTAINS_PVC: URIRef  # The item is physically marked as containing PVC (Polyvinyl chloride). Phthalate content is unspecified.
    PackagingMarkedDietAllergenCode_CONTAINS_PVC_WITHOUT_PHTHALATES: URIRef  # The item is physically marked as containing PVC (Polyvinyl chloride) without phthalates.
    PackagingMarkedDietAllergenCode_CONTAINS_PVC_WITH_PHTHALATES: URIRef  # The item is physically marked as containing PVC (Polyvinyl chloride) with phthalates.
    PackagingMarkedDietAllergenCode_DIET_PRODUCT_450_800_KCAL_PER_DAY: URIRef  # The item is physically marked that it is approved for a 450-800 kilocalorie/day diet by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_DIET_PRODUCT_800_1200_KCAL_PER_DAY: URIRef  # The item is physically marked that it is approved for a 800-1200 kilocalorie/day diet by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_GEZONDE_KEUZE_KLAVERTJE: URIRef  # Health symbol used in the Netherlands Target Market which indicates that the item is a cholesterol-reducing product.
    PackagingMarkedDietAllergenCode_HALAL: URIRef  # Indicates the product has been marked as Halal which denotes selling or serving food ritually fit according to Islamic dietary laws.
    PackagingMarkedDietAllergenCode_IK_KIES_BEWUST: URIRef  # Conscious choice symbol used in the Netherlands Target Market which may be used for products low in saturated fat, trans fatty acids, sugar and salt.
    PackagingMarkedDietAllergenCode_KOSHER: URIRef  # Indicates the product has been marked as Kosher which denotes selling or serving food ritually fit according to Jewish dietary laws.
    PackagingMarkedDietAllergenCode_LACTASE_ENZYME: URIRef  # The item is physically marked that it is approved as lactase enzyme by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_LOW_ON_PHENYLALANINE: URIRef  # The item is physically marked as containing a low level of phenylalanine as approved by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_LOW_ON_SUGAR: URIRef  # The item is physically marked as containing a low level of sugar as approved by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_MOTHERS_MILK_SUBSTITUTE: URIRef  # The item is physically marked that it is approved as substitute mother's milk the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_NUTRITION_SUPPLEMENT: URIRef  # The item is physically marked that it is approved as nutrition supplement by the appropriate authority of the target market.
    PackagingMarkedDietAllergenCode_NYCKELHAL_MARK: URIRef  # Lean product.
    PackagingMarkedDietAllergenCode_VEGETARIAN: URIRef  # Indicates the product has been marked as vegetarian which denotes a product that contains no meat, fish or other animal products.
    PackagingMarkedFreeFromCode: URIRef
    PackagingMarkedFreeFromCode_FREE_FROM_ARTIFICIAL_COLOURING: (
        URIRef  # The item is physically marked as having no artificial colouring.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_ARTIFICIAL_FLAVOURING: (
        URIRef  # The item is physically marked as having no artificial flavouring.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_ARTIFICIAL_PRESERVATIVES: (
        URIRef  # The item is physically marked as having no artificial preservatives.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_CHOLESTEROL: (
        URIRef  # The item is physically marked as having no Cholesterol.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_CLONED_FOOD: (
        URIRef  # The item is physically marked as being free from cloned food.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_DAIRY: URIRef  # The item is physically marked as being free from dairy and dairy products, as approved by the appropriate authority of the target market.
    PackagingMarkedFreeFromCode_FREE_FROM_EGG: (
        URIRef  # The item is physically marked as free from egg.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_FISH: (
        URIRef  # The item is physically marked as being free from fish.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_GLUTEN: URIRef  # The item is physically marked as free from gluten. This level of containment is frequently determined through regulation.
    PackagingMarkedFreeFromCode_FREE_FROM_LACTOSE: (
        URIRef  # The item is physically marked as being free of lactose.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_LATEX: (
        URIRef  # The item is physically marked being free from Latex (rubber).
    )
    PackagingMarkedFreeFromCode_FREE_FROM_LEGUME_PROTEIN: (
        URIRef  # The item is physically marked as being free from legume protein.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_MILK: URIRef  # The item is physically marked as being free from milk and any of its derivatives.
    PackagingMarkedFreeFromCode_FREE_FROM_MILK_PROTEIN: (
        URIRef  # The item is physically marked as being free from milk protein.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_NATURAL_GLUTEN: URIRef  # The item is physically marked as being naturally free from gluten and not extracted as part of the manufacturing process.
    PackagingMarkedFreeFromCode_FREE_FROM_PEANUTS: (
        URIRef  # The item is physically marked as being free from peanuts.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_PROTEIN: (
        URIRef  # The item is physically marked as being free from protein.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_PVC: URIRef  # The item is physically marked as being free from PVC (Polyvinyl chloride).
    PackagingMarkedFreeFromCode_FREE_FROM_SOYA: (
        URIRef  # The item is physically marked as being free from soya.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_SUGAR: (
        URIRef  # The item is physically marked as being free from sugar.
    )
    PackagingMarkedFreeFromCode_FREE_FROM_TRANSFAT: URIRef  # The item is physically marked being free from Trans Fatty Acids (Trans Fat)
    PackagingMarkedFreeFromCode_REDUCED_LACTOSE: (
        URIRef  # The item is physically marked as having a reduced amount of lactose
    )
    PackagingMarkedFreeFromCode_REDUCED_PROTEIN: (
        URIRef  # The item is physically marked as containing a low level of protein.
    )
    PackagingMarkedFreeFromCode_REDUCED_TRANSFAT: URIRef  # The item is physically marked as having a reduced amount of transfats (unsaturated).
    PackagingMarkedFreeFromCode_VERY_LOW_GLUTEN: URIRef  # The item is physically marked as a very low amount of gluten. Very low is frequently determined through regulation for example, per EU Regulation (EC) No 41/2009 [of 20 January 2009], this is defined as containing between 20 and 100 mg/kg).
    PackagingMarkedFreeFromCode_WITHOUT_ADDED_SALT: URIRef  # The item is physically marked that no salt has been added when manufacturing the product but it still can contain salt that is naturally part of the ingredients, as approved by the appropriate authority of the target market.
    PackagingMarkedFreeFromCode_WITHOUT_ADDED_SUGAR: URIRef  # The item is physically marked that no sugar has been added when manufacturing the product but it still can contain sugars that are naturally part of the ingredients, as approved by the appropriate authority of the target market.
    PackagingMarkedFreeFromCode_WITHOUT_ADDED_SWEETENER: URIRef  # The item is physically marked that no sweetener has been added when manufacturing the product.
    PackagingMarkedLabelAccreditationCode: URIRef
    PackagingMarkedLabelAccreditationCode_AMA_ORGANIC_SEAL: URIRef  # Austria Ministry of Agriculture Organic Label, AMA Marketing licenses the AMA organic logo. Red, white and black indicates the majority of ingredients are of Austrian origin.
    PackagingMarkedLabelAccreditationCode_AUS_KAUP_ESTONIA: (
        URIRef  # Used to specify Estonia Meat in their product.
    )
    PackagingMarkedLabelAccreditationCode_BDIH_LOGO: URIRef
    PackagingMarkedLabelAccreditationCode_BETER_LEVEN_1_STER: URIRef  # The one-star Beter Leven (better life) mark indicates that the product comes from a company that cares that animals are kept according to the minimal requirements for sanitation and well-being for the cattle industry.
    PackagingMarkedLabelAccreditationCode_BETER_LEVEN_2_STER: URIRef  # The two-star Beter Leven (better life) mark indicates that the product comes from a company that provides for a higher well-being of animals than that established by the minimal requirements for sanitation and well-being for the cattle industry, yet the conditions are inferior to those of Biological-class products.
    PackagingMarkedLabelAccreditationCode_BETER_LEVEN_3_STER: URIRef  # The three-star Beter Leven (better life) mark is awarded to products that come from companies that excel in keeping animals according to top guidelines for Biological-class products. In some cases this mark is accompanied by an EKO indication.
    PackagingMarkedLabelAccreditationCode_BIO_AUSTRIA_LABEL: URIRef
    PackagingMarkedLabelAccreditationCode_BIO_LABEL_GERMAN: URIRef
    PackagingMarkedLabelAccreditationCode_BIO_SUISSE_BUD_SEAL: URIRef
    PackagingMarkedLabelAccreditationCode_BLUE_ANGEL: URIRef  # The Blue Angel is awarded to companies as kind of a reward for their commitment to environmental protection. They use it to professionally promote their eco-friendly products in the market. The Blue Angel is an ecological beacon showing the consumer the way to the ecologically superior product and promotes environmentally conscious consumption.
    PackagingMarkedLabelAccreditationCode_BORD_BIA_APPROVED: URIRef  # The Bord Bia Approved logo is awarded to a company which has been audited by Bord Bia to verify that processes, from farm to fork, comply with the highest Quality Assurance Standards. These standards include animal welfare, traceability, environment, safety, feed, water, testing, inspection, hygiene and good manufacturing practice. Bord Bia Approved is awarded to a company where all the ingredients including meat content satisfy the Bord Bia requirements.
    PackagingMarkedLabelAccreditationCode_BORD_BIA_APPROVED_MEAT: URIRef  # Bord Bia Approved - Meat Content Only applies to companies where only the meat content satisfies certain conditions detailed in the Bord Bia requirements document.
    PackagingMarkedLabelAccreditationCode_BRA_MILJOVAL_LABEL_SWEDISH: URIRef  # Bra Miljoval Bra is the ecolabel of SSNC. It is referred to as Good Environmental Choice in English. SSNC started ecolabelling.
    PackagingMarkedLabelAccreditationCode_CROSSED_GRAIN_SYMBOL: URIRef  # Crossed grain logo is a trademark owned and administered by Coeliac. It is a worldwide symbol for safe gluten-free foods. Each country has their own Coeliac
    PackagingMarkedLabelAccreditationCode_DEMETER_LABEL: URIRef  # Demeter International trademark for products of certified biodynamic production.
    PackagingMarkedLabelAccreditationCode_ECOCERT_CERTIFICATE: (
        URIRef  # ECOCERT is a certification body for sustainable development.
    )
    PackagingMarkedLabelAccreditationCode_ECO_LABEL_LADYBUG: URIRef  # This is a Finnish label used by the Organic union, which represents the entire Finnish organic industry, consumers and producers in a common interest group. They work as a neutral voice in various working groups and consultations, and prepare position papers and presentations. The Federation also organizes training events and professional seminars. The Organic Federation also publishes the magazine Organic.
    PackagingMarkedLabelAccreditationCode_EC_NATIONAL_HEALTH_MARK: URIRef  # The package is physically marked with EC National Health Mark. The EC National Health Mark is the health mark for specific hygiene regulations for food of animal origin. The regulation (EC) Nr. 853/2004 of 29. April 2004 of the European Parliament on hygiene rules for food of animal origin demands that companies handling products of animal origin are authorised according to this regulation. The official body responsible for this authorisation assigns a health mark to the food producing company
    PackagingMarkedLabelAccreditationCode_EESTI_OKOMARK: URIRef  # Estonian Eco Label: Ministry of Agriculture Okomark (Label of Organic Food).
    PackagingMarkedLabelAccreditationCode_EESTI_PARIM_TOIDUAINE: URIRef  # Best Food Association of Estonia Food Industry http://www.toiduliit.ee/. An organisation that supports and promote Estonian food industry and economy, and contribute to a balanced and appropriate ethics to members of a favourable business environment for development.
    PackagingMarkedLabelAccreditationCode_EKO: URIRef  # This symbol stands for organic production certified by Skal that meets the requirements of the EU-regulation for organic production. Skal is the inspection body for the organic production in the Netherlands.
    PackagingMarkedLabelAccreditationCode_EU_ECO_LABEL: URIRef  # The item is physically marked with the European Union Eco label a European environmental initiative supported by the European Commission.
    PackagingMarkedLabelAccreditationCode_EU_ORGANIC_FARMING: URIRef  # New EU organic logo the EU introduced a new organic logo to ensure consumer protection and common standards.
    PackagingMarkedLabelAccreditationCode_FAIR_TRADE_MARK: URIRef  # The Fair Trade Mark certifies that products meet the social, economic and environmental International Fair trade Standards. The Fair Trade Mark is usually supported by a local Fair Trade Labelling Organization and certifies products not companies. It does not cover the companies or organizations selling the product
    PackagingMarkedLabelAccreditationCode_FALKEN: URIRef
    PackagingMarkedLabelAccreditationCode_FINNISH_HEART_SYMBOL: URIRef  # The heart symbol to inform the consumer at one glance that the product marked with this symbol is a preferred choice in its product group with regard to fat and sodium. Finnish Heart Association.
    PackagingMarkedLabelAccreditationCode_FOREST_STEWARDSHIP_COUNCIL_LABEL: URIRef  # The item is physically marked with the Forest Stewardship Council label.
    PackagingMarkedLabelAccreditationCode_GMO_MARKED: (
        URIRef  # The item is physically marked as of genetically modified origin.
    )
    PackagingMarkedLabelAccreditationCode_GOODS_FROM_FINLAND_BLUE_SWAN: URIRef
    PackagingMarkedLabelAccreditationCode_GREEN_DOT: URIRef
    PackagingMarkedLabelAccreditationCode_GREEN_RESTAURANT_ASSOCIATION_ENDORSED: URIRef  # The item is physically marked with the Green Restaurant Association Endorsed symbol.
    PackagingMarkedLabelAccreditationCode_GREEN_SEAL_CERTIFIED: (
        URIRef  # The item is physically marked with the Green Seal Certified symbol.
    )
    PackagingMarkedLabelAccreditationCode_GUARANTEED_IRISH: URIRef  # Ireland: The Guaranteed Irish symbol makes shopping for Irish products and services a lot easier. Shoppers know that when they buy a product or service featuring the guaranteed Irish logo they are supporting Irish companies and safeguarding Irish jobs.
    PackagingMarkedLabelAccreditationCode_KRAV_MARK: URIRef
    PackagingMarkedLabelAccreditationCode_LABEL_OF_THE_ALLERGY_AND_ASTHMA_FEDERATION: URIRef  # Allergy and Asthma Federation is a non-profit public health organisation. Our aim is to improve quality of life of the allergy and asthma patients.
    PackagingMarkedLabelAccreditationCode_LEAPING_BUNNY: URIRef  # The Coalition for Consumer Information on Cosmetics (CCIC) Leaping Bunny Program administers a cruelty-free standard and the internationally recognized Leaping Bunny Logo for companies producing cosmetic, personal care, and household products. The Leaping Bunny Program provides the best assurance that no new animal testing is used in any phase of product development by the company, its laboratories, or suppliers.
    PackagingMarkedLabelAccreditationCode_LOODUSSOBRALIK_TOODE_ESTONIA: URIRef  # Eco-friendly product The sign eco-friendly product is designed to make environmentally friendly products on store shelves more as significant. When it comes to food shall be used for agriculture, natural farming methods. No use of mineral fertilizers, insect control and plant poisons.
    PackagingMarkedLabelAccreditationCode_LOVE_IRISH_FOOD: URIRef  # Love Irish Food - a promotional label printed on the product packaging to indicate to the consumer that the food is manufactured in Ireland using Irish ingredients.
    PackagingMarkedLabelAccreditationCode_MADE_IN_FINLAND_FLAG_WITH_KEY: URIRef  # Made in Finland Products that are made in Finland Avainlippu (Key Flag) Suomalaisen Tyon
    PackagingMarkedLabelAccreditationCode_MARINE_STEWARDSHIP_COUNCIL_LABEL: URIRef
    PackagingMarkedLabelAccreditationCode_MAX_HAVELAAR: URIRef  # Fair trade symbol used in the Netherlands Target Market awarded to manufacturers which contribute to improving the living and working conditions of small farmers and agricultural workers in disadvantaged regions.
    PackagingMarkedLabelAccreditationCode_NATRUE_LABEL: URIRef  # The NATRUE Label guarantees that the products that carry it are made only with natural and organic ingredients, through soft manufacturing processes and environmentally friendly practices. The NATRUE Label is awarded by NATRUE, a non-profit organisation committed to promote and protect high standards of quality and environmental integrity.
    PackagingMarkedLabelAccreditationCode_NYCKELHALET: URIRef  # The green key hole is to be put on the healthy foods in Sweden, Denmark, and Norway within certain product groups in order to make it easier for the customers to make a healthy choice. http://www.norden.org/
    PackagingMarkedLabelAccreditationCode_OEKO_TEX_LABEL: URIRef  # Confidence in textiles. This has been the motto of the independent test institutes of the International Oeko-Tex Association since 1992, with their tests for harmful substances according to Oeko-Tex Standard 100 for textile products of all types which pose no risk whatsoever to health.
    PackagingMarkedLabelAccreditationCode_OFFICIAL_ECO_LABEL_SUN: URIRef  # Luomo Sun Sign Denotes controlled organic production. The official label of the Finnish inspection authorities; owned by the Ministry of Agriculture and Forestry.
    PackagingMarkedLabelAccreditationCode_PEFC: URIRef  # Programme for Endorsement of Forest Certification (PEFCC_ is an international non-profit, non-governmental organisation dedicated to promoting Sustainable Forest Management (SFM) through independent third-party certification
    PackagingMarkedLabelAccreditationCode_PROTECTED_DESIGNATION_OF_ORIGIN: URIRef  # The Protected designation of origin is the name of an area, a specific place or, in exceptional cases, the name of a country, used as a designation for an agricultural product or a foodstuff, the entire product must be traditionally and ENTIRELY manufactured (prepared, processed AND produced) within the specific region and thus acquire unique properties. Protected Geographical Status (PGS) is a legal framework defined in European Union law to protect the names of regional foods.
    PackagingMarkedLabelAccreditationCode_PROTECTED_GEOGRAPHICAL_INDICATION: URIRef  # The Protected geographical indication is the name of an area, a specific place or, in exceptional cases, the name of a country, used as a description of an agricultural product or a foodstuff, the entire product must be traditionally and at least PARTIALLY manufactured (prepared, processed OR produced) within the specific region and thus acquire unique properties. Protected Geographical Status (PGS) is a legal framework[1] defined in European Union law to protect the names of regional foods.
    PackagingMarkedLabelAccreditationCode_PROTECTED_HARVEST_CERTIFIED: URIRef  # The item is physically marked with the Protected Harvest Certified symbol.
    PackagingMarkedLabelAccreditationCode_QUALITY_MARK_IRELAND: URIRef  # Control IMO Organic farming is an alternative, environmentally friendly method of food production. It forbids the use of chemicals and requires production methods that respect animal welfare and do not damage the environment. The term organic can only be used on food labels in Ireland if the food product meets strict Irish and EU organic standards and is licensed by an approved certification body.
    PackagingMarkedLabelAccreditationCode_RAINFOREST_ALLIANCE: URIRef  # The item is physically marked with the Rainforest Alliance Certified symbol.
    PackagingMarkedLabelAccreditationCode_SCHARRELVLEES: URIRef  # A symbol used in the Netherlands Target Market intended for meat based products which guarantees that the animals has been growth without the use of antibiotics.
    PackagingMarkedLabelAccreditationCode_SOIL_ASSOCIATION_ORGANIC_SYMBOL: URIRef  # The Soil Association Organic Symbol is a symbol used in the UK to show that products meet a strict set of organic standards that protect health, sustainability and the environment.
    PackagingMarkedLabelAccreditationCode_SUSTAINABLE_PALM_OIL_RSPO: URIRef  # In response to the urgent and pressing global call for sustainably produced palm oil, the Roundtable on Sustainable Palm Oil (RSPO) was formed in 2004 with the objective of promoting the growth and use of sustainable oil palm products through credible global standards and engagement of stakeholders.
    PackagingMarkedLabelAccreditationCode_SVANEN: URIRef  # The Swan is the Nordic environmental label. It was established by the Nordic Council of Ministers in 1989 and Denmark joined in 1997. The Swan is used in all Nordic countries, i.e. Denmark, Norway, Sweden, Finland and Iceland.
    PackagingMarkedLabelAccreditationCode_SWEDISH_SEAL_OF_QUALITY: URIRef  # The item is physically marked with the Swedish Seal of Quality label which intends to guarantee the responsibility for the environment of the product.
    PackagingMarkedLabelAccreditationCode_TRADITIONAL_SPECIALTY_GUARANTEED: URIRef  # The Traditional specialty guaranteed is a trademark for an agricultural product or a foodstuff, which has a certain feature or a set of features, setting it clearly apart from other similar products or foodstuffs belonging to the same category. The product or foodstuff must be manufactured using traditional ingredients or must be characteristic for its traditional composition, production process, or processing reflecting a traditional type of manufacturing or processing.
    PackagingMarkedLabelAccreditationCode_TUNNUSTATUD_EESTI_MAITSE: URIRef  # Approved Estonian Taste - Quality/Tradition/Origin/Traceability for Estonian products. All raw materials must be 100% Estonian. Estonian Chamber of Agriculture and Commerce.
    PackagingMarkedLabelAccreditationCode_TUNNUSTATUD_MAITSE: URIRef  # Approved Taste label (designed as a barn swallow) denoting Estonian origin and high quality was introduced. This label has been given to products for Food quality and safety. Estonian Chamber of Agriculture and Commerce (ECAC).
    PackagingMarkedLabelAccreditationCode_UNIQUELY_FINNISH: URIRef  # Uniquely Finnish http://www.maakuntienparhaat.fi/en/ The Uniquely Finnish label is a national quality label for small entrepreneurs. ProAgria Association of Rural Advisory Centres grants the label to qualified foodstuff, handicraft and rural tourism companies based on applications.
    PackagingMarkedLabelAccreditationCode_USDA: URIRef
    PackagingMarkedLabelAccreditationCode_UTZ_CERTIFIED: URIRef  # A certification which is intended to assure the social and environmental quality in coffee production. Coffee based products may be marked with this certification.
    PackagingMarkedLabelAccreditationCode_VAELG_FULDKORN_FORST: URIRef  # Grain based foods (bread, breakfast products, baking articles etc.) which have got a high content of whole grain will be puffed with a nutritional puff from the beginning of 2009: Please choose whole grain first.
    PackagingMarkedLabelAccreditationCode_WWF_PANDA_LABEL: (
        URIRef  # Products that support the World Wildlife Federation.
    )
    PackagingMaterialDetails: URIRef  # Information on any material used for packaging.
    PackagingMaterialTypeCode: URIRef
    PackagingMaterialTypeCode_BAMBOO: URIRef  # Any of various woody or arborescent grasses (as of the genera Bambusa, Arundinaria, and Dendrocalamus of the subfamily Bambusoideae) of tropical and temperate regions having hollow stems, thick rhizomes, and shoots. The packaging may be in the form of paper, wood or leaves.
    PackagingMaterialTypeCode_CELLULOSE_HYDRATE: URIRef  # A class of materials manufactured by the conversion of natural cellulose to a soluble cellulosic derivative and subsequent regeneration, typically forming a film (e.g., cellophane).
    PackagingMaterialTypeCode_CERAMIC: URIRef  # A non-specific material made from clay and hardened by firing at a high temperatures. Examples can include Terra-cotta, Earthenware, Stoneware, Porcelain, and High-Tech Ceramics.
    PackagingMaterialTypeCode_CLOTH_OR_FABRIC: URIRef  # A non specific material made by weaving, felting, knitting, or crocheting natural and/or synthetic fibers.
    PackagingMaterialTypeCode_COMPOSITE: (
        URIRef  # A material that is made from multiple materials.
    )
    PackagingMaterialTypeCode_CORK_NATURAL: URIRef  # Cork is an impermeable buoyant material, the phellem layer of bark tissue that is harvested for commercial use primarily from Quercus suber (the cork oak).
    PackagingMaterialTypeCode_CORRUGATED_BOARD_DOUBLE_WALL: URIRef  # A structure formed by two layers of corrugated cardboard (flutes), with a linerboard facing between them.
    PackagingMaterialTypeCode_CORRUGATED_BOARD_OTHER: URIRef  # The value needed is not listed or is not defined within this list's individual code value and definitions of corrugated boards. Please send a work request into GS1 or your solution provider requesting the code you are searching for.
    PackagingMaterialTypeCode_CORRUGATED_BOARD_SINGLE_WALL: URIRef  # A structure formed by three layers of paper that are glued using starch into one single, sturdy sheet; also termed double faced.
    PackagingMaterialTypeCode_CORRUGATED_BOARD_TRIPLE_WALL: URIRef  # A structure formed by an inner and outer liner with three fluted sheets in between, each separated by a layer of paper.
    PackagingMaterialTypeCode_FIBRE_BURLAP: URIRef  # The American name for cloth woven from jute plant skins and other vegetable fibres. In other parts of the world it is known as Hessian, Hessian cloth, or gunny from the Indian gain.
    PackagingMaterialTypeCode_FIBRE_COTTON: URIRef  # A natural cellulosic seed-hair fiber, obtained from the seed pod of the cotton plant. First known in India about 3000 B.C.
    PackagingMaterialTypeCode_FIBRE_FLAX: URIRef  # The plant from the stem of which bast fiber is extracted by retting to produce linen. An erroneous term for linen fiber, particularly in blends.
    PackagingMaterialTypeCode_FIBRE_HEMP: URIRef  # Hemp is a commonly used term for varieties of the Cannabis plant. Hemp can yield fibre which can be used in ropes, cloths, weaves, as a reinforcement of polymer composites as well as pulps for paper making.
    PackagingMaterialTypeCode_FIBRE_JUTE: URIRef  # A bast fiber obtained from the round pod jute or the long pod jute of the family Tiliaceae. Jute ribbon is purely made from the jute plant. Grown extensively in Pakistan and India, mainly in the Bengal district of Pakistan.
    PackagingMaterialTypeCode_FIBRE_OTHER: URIRef  # A non specific material made of a unit of matter, either natural or manufactured, that forms the basic element of fabrics and other textile structures.
    PackagingMaterialTypeCode_FOAM: URIRef  # A non specific material in a lightweight cellular form resulting from introduction of gas bubbles during manufacture, used to reduce shock and vibration or abrasion.
    PackagingMaterialTypeCode_GLASS: URIRef  # A substance mainly consisting of sand, lime and soda, fused at high temperatures and cooled quickly so that it solidifies to a vitreous or noncrystalline condition. This term applies to transparent clear glass or as a generic term if distinction with coloured glass is not desired. Example: sodocalcite.
    PackagingMaterialTypeCode_GLASS_BOROSILICATE: URIRef  # Glass composed of silicon, boron, sodium and aluminum oxides (+ other alkaline oxides). It is a technical glass, not recyclable.
    PackagingMaterialTypeCode_GLASS_COLOURED: URIRef  # Glass containing external colouring or glass that has been coloured by the addition of colouring agents/particles in its creation
    PackagingMaterialTypeCode_GLASS_CRYSTAL: URIRef  # Glass rich in lead oxide. It is a technical glass, not recyclable, typically used in decorative objects and also in certain cosmetic packaging.
    PackagingMaterialTypeCode_LAMINATED_CARTON: URIRef  # A material made up of laminates of paperboard, foil and polyethylene which combined form a sheet suitable for asceptic processing.
    PackagingMaterialTypeCode_METAL_ALUMINUM: (
        URIRef  # A non specific material made from aluminum or aluminum alloy.
    )
    PackagingMaterialTypeCode_METAL_BRASS: (
        URIRef  # Brass is an alloy of copper and zinc.
    )
    PackagingMaterialTypeCode_METAL_COMPOSITE: URIRef  # Refers to an object that is composed of two separate metals joined together. Instead of being a mixture of two or more metals, like alloys, metal composites consist of layers of different metals.
    PackagingMaterialTypeCode_METAL_IRON: URIRef  # A heavy metallic element (Fe) capable of being fashioned into a variety of forms.
    PackagingMaterialTypeCode_METAL_LEAD: URIRef  # A bluish-white soft malleable ductile plastic but inelastic heavy metallic element (Pb)
    PackagingMaterialTypeCode_METAL_OTHER: (
        URIRef  # A non specific material made from metal or metal alloy material.
    )
    PackagingMaterialTypeCode_METAL_STAINLESS_STEEL: URIRef  # An alloy of steel with chromium and sometimes another element (as nickel or molybdenum) that is practically immune to rusting and ordinary corrosion
    PackagingMaterialTypeCode_METAL_STEEL: URIRef  # Commercial iron that contains carbon in any amount up to about 1.7 percent as an essential alloying constituent, is malleable when under suitable conditions, and is distinguished from cast iron by its malleability and lower carbon content.
    PackagingMaterialTypeCode_METAL_TIN: URIRef  # Tin is a chemical element that is obtained chiefly from the mineral cassiterite, where it occurs as an oxide, SnO2. This silvery, malleable poor metal is not easily oxidized in air, and is used to coat other metals to prevent corrosion. It is used in many alloys, most notably bronze
    PackagingMaterialTypeCode_METAL_ZAMAC: URIRef  # Zamac is a family of alloys with a base metal of zinc and alloying elements of aluminium, magnesium, and copper.
    PackagingMaterialTypeCode_MINERAL_CALCIUM_CARBONATE: URIRef  # Ground calcium carbonate and precipitated calcium carbonate products serve as functional fillers in plastic and rubber applications. Calcium carbonate is widely used as in polyvinyl chloride (PVC), polyolefin, polypropylene (PP), polyethylene (PE) and unsaturated polyester resins applications.
    PackagingMaterialTypeCode_MINERAL_OTHER: URIRef  # Any other mineral-based material not available in this list.  Should be used as a temporary measure while a proper code is established
    PackagingMaterialTypeCode_MINERAL_TALC: URIRef  # Talc is used to stiffen thermoplastics, mainly polypropylene but also polyethylene and polyamide (Nylon).
    PackagingMaterialTypeCode_NATURAL_RUBBER: URIRef  # A strong elastic material made by drying the sap from various tropical trees, especially the American rubber tree.
    PackagingMaterialTypeCode_OTHER: URIRef  # The value needed is not listed or is not defined within this list's individual code values and definitions. Please send a work request into GS1 or your solution provider requesting the code you are searching for.
    PackagingMaterialTypeCode_PAPER_CORRUGATED: (
        URIRef  # Heavy paper with ridges and grooves, used in packing fragile articles.
    )
    PackagingMaterialTypeCode_PAPER_KRAFT: URIRef  # Kraft paper is the paper grade with the highest strength. It is used for the production of e.g. paper bags, emery paper or shopping bags.
    PackagingMaterialTypeCode_PAPER_KRAFT_WET_STRENGTH: URIRef  # The wet-strength kraft paper has a certain tear strength when wet due to special additives. It is used for the production of e.g. paper bags, emery paper or shopping bags.
    PackagingMaterialTypeCode_PAPER_MOLDED_PULP: URIRef  # Used for producing pulp-based or fibrous products by pressing; example products: egg packages, trays and boxes for fruits and vegetables.
    PackagingMaterialTypeCode_PAPER_OTHER: URIRef  # Any other paper-based material not available in this list.  Should be used as a temporary measure while a proper code is established.
    PackagingMaterialTypeCode_PAPER_PAPER: URIRef  # A non-specific sheet material produced by the matting of fibres from wood, rags, or other fibrous materials.  Generally, paper is of a lesser thickness or weight than paperboard.
    PackagingMaterialTypeCode_PAPER_PAPERBOARD: URIRef  # A non specific material, generally made from cotton or wood, that describe a variety or of board materials used in the production of boxes, folding cartons, and solid fibre and corrugated shipping containers; also termed cardboard
    PackagingMaterialTypeCode_PAPER_RAYON: (
        URIRef  # Generic term for a manmade fiber derived from regenerated cellulose.
    )
    PackagingMaterialTypeCode_PLANT_LEAVES: URIRef  # Plant leaves, such as banana leaves, including wet or dry leaves. In some cases, leaves are pre-softened by steaming.
    PackagingMaterialTypeCode_PLASTIC_BIOPLASTIC: URIRef  # Plastic materials made from biomass, but may have exactly the same properties as ordinary plastic. Sometimes these plastics are biodegradable.
    PackagingMaterialTypeCode_PLASTIC_OTHER: URIRef  # A non-specific material made of any of numerous organic synthetic or processed materials that are mostly thermoplastic or thermosetting polymers of high molecular weight and that can be made into objects, films, or filaments.
    PackagingMaterialTypeCode_PLASTIC_THERMOPLASTICS: URIRef  # A non-specific substance that becomes soft and pliable when heated, without a change in its intrinsic properties. Polystyrene and polyethylene are thermoplastics.
    PackagingMaterialTypeCode_POLYMER_APET: URIRef  # Polyethylene Terephthalate, amorphous (APET) has a very high transparency, is flame retardant and suitable for direct food contact. It is used for packaging of all kinds.
    PackagingMaterialTypeCode_POLYMER_BOPP: URIRef  # Biaxially oriented PP (BOPP) films are characterized by their tear, impact and puncture resistance. The film is mainly used in food packaging, e.g. as candy wrap or wrapping for chocolate bars.
    PackagingMaterialTypeCode_POLYMER_CELLULOSE_ACETATE: URIRef  # Cellulose acetate is one of the most important esters of cellulose. Depending on the way it has been processed cellulose acetate can be used for a wide variety of applications, e.g. films, membranes or fibers.
    PackagingMaterialTypeCode_POLYMER_CPET: URIRef  # Crystallized polyethylene terephthalate (CPET) is a variation of standard PET which has been crystallized for heat resistance, rigidity, and toughness
    PackagingMaterialTypeCode_POLYMER_EPE: URIRef  # EPE is foamed polyethylene, which is a type of environmentally friendly material, that is, pearl cotton like. EPE is made of low-density polyethylene grease through a physical foaming process to produce a non-crosslinked closed cell structure. EPE can be recycled and allows a certain amount of EPE recycled material to be matched in the manufacturing process. Also known as EPE Foam.
    PackagingMaterialTypeCode_POLYMER_EPOXY: URIRef  # Epoxy resins are thermoset polymers which are frequently used as coatings for metal packaging such as soft-drink cans.
    PackagingMaterialTypeCode_POLYMER_EPS: URIRef  # Expanded polystyrene is a rigid, tough, closed cell and lightweight thermoplastic foam material. It is manufactured by expanding spherical beads in a mold, using heat and pressure to fuse the beads together. While each individual bead is a closed cell environment, there are significant open spaces between each bead.
    PackagingMaterialTypeCode_POLYMER_EVA: URIRef  # Ethylene vinyl acetate, a copolymer of 60 to 90% ethylene and 40 to 10% vinyl acetate.  Packaging applications include soft films, coatings, hot melt adhesives, wine cork substitutes, and closure seals for plastic and metal container caps.
    PackagingMaterialTypeCode_POLYMER_EVOH: URIRef  # Ethylene vinyl alcohol, a copolymer of ethylene and vinyl alcohol. A plastic resin commonly used in food applications to provide barrier to oxygen and other gases.
    PackagingMaterialTypeCode_POLYMER_HDPE: URIRef  # High-Density PolyEthylene (HDPE) is a polyethylene thermoplastic made from petroleum.  A strong, relatively opaque form of polyethylene having a dense structure with few side branches off the main carbon backbone. Can be applied to bottles, flasks and caps.
    PackagingMaterialTypeCode_POLYMER_IONOMER: URIRef  # Ionically is a cross-linked polyethylene (ionomer), can be used in combination with PE for its barrier properties.
    PackagingMaterialTypeCode_POLYMER_LDPE: URIRef  # Low-density polyethylene (LDPE) is a polyethylene thermoplastic made from petroleum.  A strong form of polyethylene having a less dense structure with more side branches off the main carbon backbone (on about 2% of the carbon atoms) than HDPE; therefore its tensile strength is lower, and its resilience is higherMade in translucent or opaque variations, it is quite flexible, and tough to the degree of being almost unbreakable.  It is widely used for manufacturing various containers, dispensing bottles, wash bottles, tubing, plastic bags for computer components, and various moulded laboratory equipment. Its most common use is in plastic bags.
    PackagingMaterialTypeCode_POLYMER_LLDPE: URIRef  # Linear low density polyethylene is a linear polyethylene with a significant number of short branches on the polymer backbone. It is commonly made by copolymerization of ethylene with longer-chain olefins. It is different from LDPE due to the absence of long chain branches which gives it higher tensile strength, impact and puncture resistance than LDPE. Common uses of LLDPE are plastic bags, wraps, stretch wraps, pouches, covers and lids.
    PackagingMaterialTypeCode_POLYMER_MDPE: URIRef  # Medium-density polyethylene is a type of polyethylene defined by a density range of 0.926-0.940 g/cm3. MDPE is typically used in shrink films, sacks, packaging film and carrier bags.
    PackagingMaterialTypeCode_POLYMER_MIX: URIRef  # A polymer blend or mixture of least two polymers that are blended to create a new material with different physical properties. These tend to be a proprietary mix of polymers and cannot be separated. The individual materials may not be known by the seller.
    PackagingMaterialTypeCode_POLYMER_NYLON: URIRef  # Packaging applications include oven-baking bags (nylon 6 and nylon 66) and barrier layers (MXD6 and nylon 6) for PET and HDPE bottles. Very occasionally, bottles can be made of nylon.
    PackagingMaterialTypeCode_POLYMER_OPP: URIRef  # Oriented polypropylene (OPP) is made of a soft polypropylene material which is stretched in a transverse or longitudinal direction (monoaxial) and becomes therefore brittle. Also known as: biaxially oriented polypropylene (BOPP), CAS Registry Number: 9003-07-0
    PackagingMaterialTypeCode_POLYMER_OTHER: URIRef  # A non-specific chemical compound or mixture of compounds formed by polymerization and consisting essentially of repeating structural units
    PackagingMaterialTypeCode_POLYMER_PA: URIRef  # A polymer with repeating units linked by amide bonds. Polyamides (PA) occur both naturally and artificially, examples of naturally occurring polyamides are proteins, such as wool and silk. Artificially made polyamides can be  nylons, aramids, and sodium poly(aspartate).
    PackagingMaterialTypeCode_POLYMER_PAN: URIRef  # Polyacrylonitril is a organic polymer which is frequently used in fibres for textiles. As fibres the material is frequently referred to as Acrylic.
    PackagingMaterialTypeCode_POLYMER_PC: URIRef  # Polycarbonate, a transparent thermoplastic which is used in a wide variety of applications including CDs and DVDs, eyeglasses, cell phone covers, laptops as well as packaging applications such as bottles.
    PackagingMaterialTypeCode_POLYMER_PCL: URIRef  # Polycaprolactone is a biodegradable polyester which is also used in in the manufacturing of polyurethanes. It is also used in blends with thermoplastic starch to improve properties and can also be used as a plasticizer to PVC.
    PackagingMaterialTypeCode_POLYMER_PE: (
        URIRef  # A thermoplastic composed of the polymers of ethylene.
    )
    PackagingMaterialTypeCode_POLYMER_PEN: URIRef  # Polyethylene naphthalate is a polymer with good barrier properties (unlike Polyethylene terephthalate). It is well-suited for production of the amber-colored bottles meant for packing beverages like beer.
    PackagingMaterialTypeCode_POLYMER_PET: URIRef  # Polyethylene terephthalate is a thermoplastic polymer resin of the polyester family and is used in synthetic fibers. Can be applied to bottles, flasks and caps.
    PackagingMaterialTypeCode_POLYMER_PETG: URIRef  # Polyethylene Terephthalate Glycol (PETG) is a PET modified with glycol, which is characterized by its aqueous properties (viscosity). Applications are found in injection molding.
    PackagingMaterialTypeCode_POLYMER_PHA: URIRef  # Polyhydroxyalkanoates are linear polyesters produced in nature by bacterial fermentation of sugar or lipids.
    PackagingMaterialTypeCode_POLYMER_PLA: URIRef  # Polylactic acid or Polylactide is a biodegradable, thermoplastic, aliphatic polyester derived from lactic acid.
    PackagingMaterialTypeCode_POLYMER_PMMA: URIRef  # Polymethyl Methacrylate (PMMA) is often used as a lightweight and shatterproof alternative to glass, due to its transparency, brilliance and scratch resistance, PMMA is therefore often referred to as acrylic glass.
    PackagingMaterialTypeCode_POLYMER_POM: URIRef  # Polyoxymethylene (POM) is a thermoplastic with good mechanical properties and high dimensional stability. Fields of application are the automotive industry and electrical engineering, in packaging it is used for e.g. spray cans, gas lighter tanks, gas ampoules. Also known as acetal, polyacetal, and polyformaldehyde.
    PackagingMaterialTypeCode_POLYMER_PP: URIRef  # A non-specific material made of various thermoplastic plastics or fibers that are polymers of propylene.
    PackagingMaterialTypeCode_POLYMER_PS: URIRef  # A polymer prepared by the polymerization of styrene as the sole monomer
    PackagingMaterialTypeCode_POLYMER_PU: URIRef  # Polyurethanes are primarily thermoset resins which are used in the manufacture of flexible and rigid foams, microcellular foam seals and gaskets, as well as high performance adhesives, surface coatings and sealants. Polyurethane can also be used to make synthetic fibers.
    PackagingMaterialTypeCode_POLYMER_PVA: URIRef  # Polyvinyl alcohol (PVA or PVOH) is a biodegradable and highly water soluble polymer with high gas and grease barrier. Common uses for PVA are paper adhesives, paper coatings, as a self-standing water soluble films as well as blends to improve processability of thermoplastic starch.
    PackagingMaterialTypeCode_POLYMER_PVC: URIRef  # A polymer of vinyl chloride used especially for electrical insulation, films, and pipes
    PackagingMaterialTypeCode_POLYMER_PVDC: URIRef  # Polyvinylidene chloride is primarily used as a barrier coating to provide barrier against fat, vapour and gases.
    PackagingMaterialTypeCode_POLYMER_SAN: URIRef  # Styrene acrylonitrile (SAN) is a copolymer transparent and rigid plastic. Examples of applications are kitchenware and cosmetic packaging.
    PackagingMaterialTypeCode_POLYMER_SILICONE: URIRef  # Polymer is generally composed of organic chains linked together by the silicon-oxygen bond. Used in particular for valves. Also know as polysiloxane.
    PackagingMaterialTypeCode_POLYMER_TPS: URIRef  # Thermoplastic starch is obtained through destructurization of natural starch through exposure to shear and heat. TPS is most frequently used in blends with biodegradable synthetic polymers such as PCL and PVA.
    PackagingMaterialTypeCode_POLYMER_XPS: URIRef  # Extruded polystyrene is a rigid, tough, closed cell and lightweight thermoplastic foam material. It is manufactured using a process of extrusion that produces a homogeneous 'closed cell' matrix with each cell fully enclosed by polystyrene walls.
    PackagingMaterialTypeCode_RUBBER: URIRef  # A strong elastic synthetic substance made either by improving the qualities of natural rubber or by an industrial process using petroleum and coal products
    PackagingMaterialTypeCode_VINYL: URIRef  # A non-specific polymer of a vinyl compound or a product (as a resin or a textile fiber) made from such a polymer
    PackagingMaterialTypeCode_WOOD_HARDBOARD: URIRef  # Hardboard (not to be confused with hardwood), also called High-Density Fiberboard (HDF), is a type of fiberboard, which is similar to particle board and medium-density fiberboard, but is denser, much stronger and harder because it is made out of exploded wood fibers which have been highly compressed. Consequently, the density of hardboard is 31 lbs or more per cubic foot (500 kg/m_)[2] and is usually about 50-65 lbs per cubic foot (800-1040 kg/m_). It differs from particle board in that the bonding of the wood fibers requires no additional materials, although resin is often added. Unlike particle board, it will not split or crack.
    PackagingMaterialTypeCode_WOOD_HARDWOOD: URIRef  # A general term referring to any variety of broad-leaved, deciduous trees, and the wood from those trees. The term has nothing to do with the actual hardness of the wood; some hardwoods are softer than certain softwood (evergreen) species.
    PackagingMaterialTypeCode_WOOD_MEDIUM_DENSITY_FIBREBOARD: URIRef  # Medium-Density Fibreboard (MDF) is an engineered wood product made by breaking down hardwood or softwood residuals into wood fibres, combining them with wax and a resin binder, and forming panels by applying high temperature and pressure. MDF is generally denser than plywood. It is made up of separated fibres, but can be used as a building material similar in application to plywood. It is stronger and much more dense than particle board.
    PackagingMaterialTypeCode_WOOD_ORIENTED_STRANDBOARD: URIRef  # Oriented Strand Board (OSB), also known as sterling board, sterling OSB, aspenite, and smartply, is an engineered wood particle board formed by adding adhesives and then compressing layers of wood strands (flakes) in specific orientations. OSB may have a rough and variegated surface with the individual strips of around 2.5 - 15 cm (1 - 6 inch), lying unevenly across each other and comes in a variety of types.
    PackagingMaterialTypeCode_WOOD_OTHER: URIRef  # A non specific material made from the hard fibrous lignified substance under the bark of trees.
    PackagingMaterialTypeCode_WOOD_PARTICLE_BOARD: URIRef  # Particle Board, also known as particleboard, chipboard, and Low-Density Fiberboard (LDF), is an engineered wood product manufactured from wood chips, sawmill shavings, or sawdust, and a synthetic resin or other suitable binder, which is pressed and extruded. Particle board is a composite material.
    PackagingMaterialTypeCode_WOOD_PLYWOOD: URIRef  # Plywood, a manufactured wood panel similar to LDF, MDF, and HDF, is made from layering thin sheets of wood. Plywood layers (called veneers or plies) are glued together, with adjacent plies having their wood grain rotated relative to adjacent layers up to 90 degrees.  All plywoods bind resin and wood fibre sheets (cellulose cells are long, strong and thin) to form a composite material.
    PackagingMaterialTypeCode_WOOD_SOFTWOOD: URIRef  # General term used to describe lumber produced from needle and/or cone bearing trees (Conifers).
    PackagingRecyclingProcessTypeCode: URIRef
    PackagingRecyclingProcessTypeCode_COMPOSTABLE: URIRef  # Packaging that can biodegrade generating a relatively homogeneous and stable humus-like substance.
    PackagingRecyclingProcessTypeCode_ENERGY_RECOVERABLE: URIRef  # Packaging which allows for a net calorific gain in energy recovery operations.
    PackagingRecyclingProcessTypeCode_RECYCLABLE: URIRef  # Packaging material and format which can be diverted from the waste stream through available processes and programmes and can be collected, processed and returned to use in the form of raw materials or products.
    PackagingRecyclingProcessTypeCode_REUSABLE: URIRef  # Packaging that has been conceived and designed to accomplished within its life cycle a certain number of trips, rotations or uses for the same purpose for which it was conceived.
    PackagingRecyclingSchemeCode: URIRef
    PackagingRecyclingSchemeCode_ALKO: URIRef  # Alko inc. is an independent, entirely State-owned company. Alko is administered and supervised by the Ministry of Social Affairs and Health. They have own recycling system for alcohol products bottles called Alko. This is a recycling system used in Finland
    PackagingRecyclingSchemeCode_A_PULLO: URIRef  # PALPA stands for Suomen Palautuspakkaus Oy. PALPA administers the recycling of beverage containers and promotes recycling in Finland. A-pullo is one of the recycling systems. PALPA is the administrator. This is a recycling system used in Finland.
    PackagingRecyclingSchemeCode_EKO_PULLO: URIRef  # PALPA Standas for Suomen Palautuspakkaus Oy. PALPA administers the recycling of beverage containers and promotes recycling in Finland. EKO-pullo is one of the recycling systems PALPA is administer. This is a recycling system used in Finland.
    PackagingRecyclingSchemeCode_PALPA: URIRef  # PALPA stands for Suomen Palautuspakkaus Oy. PALPA administers the recycling of beverage containers and promotes recycling in Finland. PALPA is on of the recycling systems PALPA is administer. This is a recycling system used in Finland.
    PackagingShapeCode: URIRef
    PackagingShapeCode_BAR: (
        URIRef  # A relatively long, evenly shaped piece of some solid substance
    )
    PackagingShapeCode_COIL: URIRef  # A spiral structure made by winding a material into a series of loops. A coil may or may not have a spindle around which the loops are formed.
    PackagingShapeCode_CONE: URIRef  # A cone is a three-dimensional geometric shape that tapers smoothly from a flat, round base to a point.
    PackagingShapeCode_CYLINDRICAL: URIRef  # A long shape that has a circular base and an equally-sized circular top.
    PackagingShapeCode_POLYGON: URIRef  # A plane figure that is bounded by a closed path or circuit composed of a finite sequence of equally-sized straight line segments. A polygon may have a varying number of segments or faces resulting in different configurations, for example a 5-faced polygon: pentagon, 6-faced: hexagon, 8-faced: octagon, 12-faced: dodecahedron, etc.
    PackagingShapeCode_RECTANGULAR: (
        URIRef  # A closed planar quadrilateral with four right angles.
    )
    PackagingShapeCode_SPHERICAL: URIRef  # A perfectly round geometrical object in three-dimensional space, such as the shape of a round ball. Like a circle in two dimensions, a perfect sphere is completely symmetrical around its centre, with all points on the surface lying the same distance from the centre point.
    PackagingShapeCode_TABLET: URIRef  # The result of different materials being compressed into a solid block usually of small dimensions.
    PackagingShapeCode_UNSPECIFIED: URIRef  # Shape is not currently specified in the list. To be used as a temporary means until a specific missing value is added to the list.
    PaymentMethod: URIRef  # A code indicating an accepted method of payment
    PaymentMethod_BANKERS_DRAFT: (
        URIRef  # Issue of a banker's draft in payment of the funds.
    )
    PaymentMethod_BANK_CHEQUE: URIRef  # Payment by a pre-printed form, which has been completed by a financial institution, on which instructions are given to an account holder (a bank or building society) to pay a stated sum to a named recipient.
    PaymentMethod_BANK_GIRO: URIRef  # The payment was originally made by bankgiro.
    PaymentMethod_BOOKENTRY_CREDIT: URIRef  # House Credit.
    PaymentMethod_BOOKENTRY_DEBIT: URIRef  # House Debit.
    PaymentMethod_BOP: URIRef
    PaymentMethod_CASH: URIRef  # Payment by currency (including bills and coins) in circulation, including checking account deposits.
    PaymentMethod_CERTIFIED_CHEQUE: URIRef  # Payment by a pre-printed form stamped with the paying bank's certification on which instructions are given to an account holder (a bank or building society) to pay a stated sum to a named recipient .
    PaymentMethod_CHEQUE: URIRef  # Payment by a pre-printed form on which instructions are given to an account holder (a bank or building society) to pay a stated sum to a named recipient.
    PaymentMethod_CREDIT_CARD: URIRef  # Payment by means of a card issued by a bank or other financial institution.
    PaymentMethod_CREDIT_CARD_AMEX: URIRef  # Payment by American Express credit card
    PaymentMethod_CREDIT_CARD_DINERS_CLUB: URIRef  # Payment by Diners Club credit card
    PaymentMethod_CREDIT_CARD_DISCOVER: URIRef  # Payment by Discover credit card
    PaymentMethod_CREDIT_CARD_MASTERCARD: URIRef  # Payment by Mastercard credit card
    PaymentMethod_CREDIT_CARD_VISA: URIRef  # Payment by Visa credit card
    PaymentMethod_DEBIT_CARD: URIRef  # The amount is to be, or has been, directly debited to the customer's bank account through a bank card.
    PaymentMethod_DEBIT_CARD_MAESTRO: URIRef  # Payment by Maestro debit card
    PaymentMethod_DEBIT_CARD_MASTERCARD: URIRef  # Payment by Mastercard debit card
    PaymentMethod_DEBIT_CARD_VISA: URIRef  # Payment by Visa debit card
    PaymentMethod_DEBIT_CARD_VISA_ELECTRON: (
        URIRef  # Payment by Visa Electron debit card
    )
    PaymentMethod_ELECTRONIC_CREDIT_ACH: (
        URIRef  # A credit transaction made through the automated clearing house system
    )
    PaymentMethod_ELECTRONIC_DEBIT_ACH: (
        URIRef  # A debit transaction made through the automated clearing house system.
    )
    PaymentMethod_FED_WIRE_NON_REPETITIVE: URIRef  # Fedwire is a real time gross settlement funds transfer system operated by the Federal Reserve Banks that enables financial institutions to electronically transfer funds between its participants.
    PaymentMethod_FED_WIRE_REPETITIVE: URIRef  # Repetitive Fedwire is a real time gross settlement funds transfer system operated by the Federal Reserve Banks that enables financial institutions to electronically transfer funds between its participants. Repetitive wire transfers are sent by the same party to the same recipient through the same financial institution with the same wiring instructions
    PaymentMethod_INTERNATIONAL_WIRE: URIRef  # Payment by international wire transfer
    PaymentMethod_LETTER_OF_CREDIT: (
        URIRef  # The financial operation is a letter of credit.
    )
    PaymentMethod_ONLINE_PAYMENT: URIRef  # Payment by online payment mechanisms
    PaymentMethod_ONLINE_PAYMENT_APPLE_PAY: URIRef  # Online payment via Apple Pay
    PaymentMethod_ONLINE_PAYMENT_GOOGLE_WALLET: (
        URIRef  # Online payment via Google Wallet
    )
    PaymentMethod_ONLINE_PAYMENT_PAYPAL: URIRef  # Online payment via PayPal
    PaymentMethod_POSTGIRO: URIRef  # The financial operation has been done by postgiro.
    PaymentMethod_WIRE_TRANSFER_CREDIT: URIRef  # Payment by wire transfer credit
    PaymentMethod_WIRE_TRANSFER_DEBIT: URIRef  # Payment by wire transfer debit
    Place: URIRef  # Entities that have a somewhat fixed, physical location.
    PostalAddress: URIRef  # The location at which a particular organization or person may be found or reached.
    Power: URIRef  # The rate of doing work or rate of production, transfer or consumption of energy; the amount of energy transferred or converted per unit time.  SI Units: watt
    PreparationTypeCode: URIRef  # A code indicating a method of preparation of a food or beverage product
    PreparationTypeCode_AS_DRAINED: URIRef  # The state of the product after it has been separated from any liquid within the package. For example, a can of apricots in syrup would have a different nutritional composition if the apricots are consumed with the syrup rather than if the syrup is drained before consuming the apricots (because of the high sugar and energy content of the syrup).
    PreparationTypeCode_BAKE: (
        URIRef  # Cooking food in an oven by dry heat applied evenly throughout the oven
    )
    PreparationTypeCode_BARBECUE: (
        URIRef  # Method of cooking meat with the heat and hot gasses of a fire
    )
    PreparationTypeCode_BLANCH: URIRef  # Food preparation wherein the food substance is rapidly plunged into boiling water and then removed after a brief, timed interval and then plunged into iced water or placed under cold running water
    PreparationTypeCode_BLIND_BAKE: (
        URIRef  # Baking a pie crust or other pastry without the filling
    )
    PreparationTypeCode_BOIL: URIRef  # Cooking food in boiling water, or other water-based liquid such as stock or milk
    PreparationTypeCode_BRAISE: URIRef  # Cooking with moist heat, typically in a covered pot with a small amount of liquid
    PreparationTypeCode_BROIL: URIRef  # Cooking food with high heat with the heat applied directly to the food, most commonly from above. Heat transfer to the food is primarily via radiant heat
    PreparationTypeCode_DEEP_FRY: (
        URIRef  # Cooking method whereby food is submerged in hot oil or fat.
    )
    PreparationTypeCode_DOUBLE_STEAM: URIRef  # Cooking technique to prepare delicate food such as bird nests, shark fins etc. The food is covered with water and put in a covered ceramic jar
    PreparationTypeCode_FREEZE: (
        URIRef  # Convert the product from room temperature to a frozen state.Simple
    )
    PreparationTypeCode_FRY: URIRef  # Cooking of food in fat.
    PreparationTypeCode_GRIDDLE_FRY: (
        URIRef  # Form of cooking where the food is fried with its own fat.
    )
    PreparationTypeCode_GRILL: URIRef  # Form of cooking that involves direct heat. The definition varies widely by region and culture
    PreparationTypeCode_HEAT_AND_SERVE: URIRef  # Prepare the item by simply heating or warming to a desired temperature or visual state prior to serving
    PreparationTypeCode_MICROWAVE: (
        URIRef  # Cooking food by employing microwave radiation
    )
    PreparationTypeCode_PAN_FRY: URIRef  # Form of frying characterised by the use of less cooking oil than deep frying
    PreparationTypeCode_POACH: URIRef  # Cooking food by gently simmering food in liquid, generally water, stock or wine
    PreparationTypeCode_PREPARED: URIRef  # The state of the product after preparation (e.g. after adding milk or water).
    PreparationTypeCode_PRESSURE_COOK: URIRef  # Method of cooking in a sealed vessel that does not permit air or liquids to escape below a preset pressure
    PreparationTypeCode_PRESSURE_FRY: URIRef  # Meat and cooking oil are brought to high temperatures while pressure is held high enough that the water within is prevented from boiling off
    PreparationTypeCode_READY_TO_DRINK: URIRef  # No Preparation. The product is ready for use after being taken out of the packaging (if packaging exists) without the need of any further action prior to consumption or use
    PreparationTypeCode_READY_TO_EAT: (
        URIRef  # Besides unpacking no additional preparation required.
    )
    PreparationTypeCode_RECONSTITUTE: URIRef  # Restore a dry or concentrated food to its original strength or consistency by adding water.
    PreparationTypeCode_REFRIGERATE: (
        URIRef  # Convert the product from room temperature to a chilled state.
    )
    PreparationTypeCode_ROAST: URIRef  # Cooking method that uses dry heat, whether an open flame, oven, or other heat source.
    PreparationTypeCode_ROTISSERIE: URIRef  # Style of roasting where meat is skewered on a spit and revolves over a flame
    PreparationTypeCode_SAUTE: URIRef  # Cooking food using a small amount of fat in a shallow pan over relatively high heat
    PreparationTypeCode_SEAR: URIRef  # Technique used in grilling, roasting, braising, sauteing, etc. That cooks the surface of the food (usually meat, poultry or fish) at high temperature so that a caramelised crust forms
    PreparationTypeCode_SIMMER: URIRef  # Cook food by heating it in water kept just below the boiling point (same as coddling)
    PreparationTypeCode_SMOKE: URIRef  # Process of curing, cooking, or seasoning food by exposing it for long periods of time to the smoke from a wood fire
    PreparationTypeCode_STEAM: URIRef  # Cooking by first boiling the water so it will evaporate into steam, then the steam will carry heat to the food, thus achieving heating the food
    PreparationTypeCode_STEW: URIRef  # Preparing meat cut into smaller pieces or cubes by simmering it in liquid, usually together with vegetables
    PreparationTypeCode_STIR_FRY: (
        URIRef  # Chinese cooking technique used because of its fast cooking speed
    )
    PreparationTypeCode_THAW: URIRef  # Convert the product from a frozen state to a chilled or room temperature state.
    PreparationTypeCode_UNPREPARED: URIRef  # The initial state of the product.
    PreparationTypeCode_UNSPECIFIED: URIRef  # Unknown, not applicable
    PreservationTechniqueCode: URIRef
    PreservationTechniqueCode_ACIDIFICATION: URIRef  # Dropping pH of food
    PreservationTechniqueCode_ALCOHOL_CURING: (
        URIRef  # Treatment of food by adding alcohol in order to preserve the product
    )
    PreservationTechniqueCode_ATTESTED_MILK: URIRef  # Raw Milk (without heat treatment)
    PreservationTechniqueCode_BOILING: URIRef  # Cooking
    PreservationTechniqueCode_BRINING: (
        URIRef  # Water saturating or strongly impregnating with salt
    )
    PreservationTechniqueCode_CANNING: URIRef  # Preserved in a sealed airtight container, usually made of tin-coated iron
    PreservationTechniqueCode_COLD_SMOKE_CURING: (
        URIRef  # To smoke the food at between 70 degrees to 90 degrees F.
    )
    PreservationTechniqueCode_CONSERVE: URIRef  # Keep from harm or damage
    PreservationTechniqueCode_DEHYDRATION: URIRef  # To remove water from food
    PreservationTechniqueCode_DRYING: (
        URIRef  # Making with moisture having evaporated, drained away
    )
    PreservationTechniqueCode_FERMENTATION: URIRef  # Any of a group of chemical reactions induced by living or nonliving ferments that split complex organic compounds into relatively simple substance
    PreservationTechniqueCode_FREEZE_DRYING: (
        URIRef  # Preserving food by freezing and then drying in a vacuum
    )
    PreservationTechniqueCode_FREEZING: (
        URIRef  # Turning into ice or another solid by cold
    )
    PreservationTechniqueCode_HIGH_TEMPERATURE_TREATED_MILK: URIRef  # Legally also pasteurisation, MHD for longer (about 2 to 3 weeks), ESL-milk
    PreservationTechniqueCode_HOT_SMOKE_CURING: URIRef  # Hot-smoking partially or totally cooks the food by treating it at temperatures ranging from 100 degrees to 190 degrees F.
    PreservationTechniqueCode_IONISATION: URIRef  # To convert into an ion or ions
    PreservationTechniqueCode_IRRADIATION: URIRef  # Food irradiation is the process of exposing food to ionising radiation in order to disinfest, sterilise, or preserve food.
    PreservationTechniqueCode_PASTEURISATION: (
        URIRef  # Partially sterilisation by heating
    )
    PreservationTechniqueCode_QUICK_FREEZING: (
        URIRef  # Freezing (food) rapidly so as to preserve its qualities
    )
    PreservationTechniqueCode_SALT_CURING: URIRef  # Preserving by using a salt brine
    PreservationTechniqueCode_SOUS_VIDE: (
        URIRef  # Low temperature long time cooking under vacuum
    )
    PreservationTechniqueCode_STERILISATION: URIRef  # A process that effectively kills or eliminates transmissibleagents (such as fungi, bacteria, viruses, spore forms, etc.).
    PreservationTechniqueCode_SUGAR_CURING: (
        URIRef  # Treatment of food by adding sugar in order to preserve the product
    )
    PreservationTechniqueCode_ULTRA_HIGH_TEMPERATURE: (
        URIRef  # Ultra heat treated (especially for milk)
    )
    PreservationTechniqueCode_UNDER_MODIFIED_ATMOSPHERE: (
        URIRef  # Packed with a gas with protective proprieties
    )
    PreservationTechniqueCode_VACUUM_PACKED: (
        URIRef  # Sealed after the partial removal of air
    )
    Pressure: URIRef  # The perpendicular force per unit area acting on a material and tending to change its dimensions.  SI Units: pascal, newton per square metre
    PriceSpecification: URIRef  # A structured value representing a monetary amount, consisting of a value and currency code.
    Product: URIRef  # Any item (product or service) upon which there is a need to retrieve pre-defined information and that may be priced, or ordered, or invoiced at any point in any supply chain.
    ProductYieldDetails: URIRef  # A grouping of properties related to the yield of a food or beverage product according to a specified type of preparation.
    ProductYieldTypeCode: URIRef
    ProductYieldTypeCode_AFTER_COOKING: (
        URIRef  # Weight or volume of food product after it has been prepared.
    )
    ProductYieldTypeCode_AFTER_DILUTION: (
        URIRef  # Volume of food product after a fluid has been added.
    )
    ProductYieldTypeCode_DRAINED_WEIGHT: URIRef  # Weight of food product after the fluid in which the food product was preserved has been removed.
    ProductYieldTypeCode_UNSPECIFIED: (
        URIRef  # Product yield type is unknown or irrelevant
    )
    QuantitativeValue: URIRef  # A point value or interval for product characteristics and other purposes. A unit of measurement is also specified.
    RadiantFlux: URIRef  # The total power emitted, received or passing in the form of electromagnetic radiation; a measure of electromagnetic energy per unit time.  SI Units: watt
    RadiantIntensity: URIRef  # The radiant flux per unit solid angle emitted by a point source.  SI Units: watt / steradian
    Radioactivity: URIRef  # The rate of spontaneous disintegration or decay of certain natural heavy elements, accompanied by alpha-rays, beta-rays or gamma-rays.  SI Units: becquerel
    ReferencedFileDetails: (
        URIRef  # Provides URL and other information on a referenced electronic file.
    )
    ReferencedFileTypeCode: URIRef
    ReferencedFileTypeCode_360_DEGREE_IMAGE: (
        URIRef  # Allows x-axis interactive rotation of product via website.
    )
    ReferencedFileTypeCode_AMBIENCE_MOOD_IMAGE: URIRef  # Trade Item image representing the image the manufacturer is supplying to the consumer to invoke a connection to the item by setting a 'mood' or feeling for the item and its use.
    ReferencedFileTypeCode_APPLICATION_IMAGE: URIRef  # Trade Item image representing the image the manufacturer is supplying to the consumer to depict how the product itself is used.
    ReferencedFileTypeCode_ASSEMBLY_INSTRUCTIONS: URIRef  # Link to a file the explains how to assemble (put together) the trade item.
    ReferencedFileTypeCode_AUDIO: URIRef  # Link to a file containing an audio clip which is relevant to the product. Examples are commercials, or instructional/ how to use audio files.
    ReferencedFileTypeCode_AWARD_CERTIFICATE: URIRef  # The award certificate is a written document created by the Award Committee that describes the terms and conditions of the Award. Example: http://www.cronierwines.com/awards-in-2016/
    ReferencedFileTypeCode_BARCODE: URIRef  # Link to a file containing a visual representation of the barcode which is on the product or its packaging.
    ReferencedFileTypeCode_CERTIFICATION: URIRef  # Document which contains a special certification by a third party (e.g. International Food Standard [IFS], QS-Approval Mark for meat product, sausage, fruit, vegetables and potatoes or bio audits).
    ReferencedFileTypeCode_CHEMICAL_ASSESSMENT_SUMMARY: URIRef  # Link to a file containing the chemical ingredient information sent to the supplier from a third party as a result of the assessment.
    ReferencedFileTypeCode_CHEMICAL_SAFETY_REPORT: URIRef  # Link to the file containing a report detailing the risks arising from the manufacture and/or use of a substance and to ensure that they are adequately controlled.
    ReferencedFileTypeCode_CHILD_NUTRITION_LABEL: URIRef  # Link to a file containing the Child Nutrition Label as formatted according to regulations and rules of an appropriate regulatory body for the target market.
    ReferencedFileTypeCode_CLEANING_DISINFECTION_STERILISATION_INSTRUCTIONS: URIRef  # The cleaning, disinfection and/or sterilisation instructions that apply to the product. These may be in accordance with EN-ISO 17664.
    ReferencedFileTypeCode_CLINICIAN_MEDICINE_INFORMATION: URIRef  # A clinician focused product information document that is written by the pharmaceutical company responsible for the medicine. This document is intended to assist doctors, pharmacists and other health professionals in prescribing and dispensing medicines. In addition, this information can be used by health professionals in their consultations with patients, so that the patient can be better informed about their medicines.
    ReferencedFileTypeCode_CONSUMER_HANDLING_AND_STORAGE: URIRef  # Link to a website, file, or image containing the manufacturer's recommendations for how the consumer or end user should store and handle the product.
    ReferencedFileTypeCode_CONTENT_TEXTURE_IMAGE: URIRef  # Trade Item image representing the image the manufacturer is supplying to the consumer to depict the content or texture of an item. The image should be designed in such a way that the texture can be experienced by the consumer similar to stationary retail, e.g. creme, lipstick.
    ReferencedFileTypeCode_CROSSSECTION_VIEW: URIRef  # A picture of a trade item with a cut away vertical plane removed (e.g. Cross-section of a Tire revealing steel belts and tire tread detail).
    ReferencedFileTypeCode_DECLARATION_OF_CONFORMITY: URIRef  # A Declaration of Conformity is a document in which the manufacturer states that the product satisfies the essential requirements of the applicable legislation(s), e.g. for toys, medical devices or electrical equipment. By drawing up and signing the EU Declaration of Conformity, the manufacturer assumes responsibility for the compliance of the product. For more information please see https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R1020&from=DE
    ReferencedFileTypeCode_DIET_CERTIFICATE: URIRef  # Link to a website or file containing a diet certificate granted to the product
    ReferencedFileTypeCode_DISPOSAL_INSTRUCTIONS: URIRef  # Link to a website, file or instruction movie how to dispose a product properly or how to clean up a broken product in case the product contains materials like mercury.
    ReferencedFileTypeCode_DOCUMENT: URIRef  # Link to a document or text file containing product information. Examples of this type could be an instruction manual, assembly guide, or warranty document.
    ReferencedFileTypeCode_DOP_SHEET: URIRef  # Link to a file containing the product's Declaration of Performance Sheet (DOP). This file can be either an image or a document.
    ReferencedFileTypeCode_DRUG_FACT_LABEL: URIRef  # The file link is to a drug fact panel of the trade item. A drug fact label usually contains such items as active ingredients, uses, warnings, purpose, directions, etc.
    ReferencedFileTypeCode_ECOLOGICAL_FACT_SHEET: URIRef  # Link to a file containing the details of a product with its environmental impact and performance. E.g. Beelong.ch Eco-Score Fact Sheet.
    ReferencedFileTypeCode_ENERGY_LABEL: URIRef  # Link to the energy label for a trade item.  On 19 May 2010, the EU adopted the Directive 2010/30/EU on energy labels. Energy labels help consumers choosing products which save energy and thus money. They also provide incentives for the industry to develop and invest in energy efficient product design. They are found on a selection of white goods and other products and are designed to help customers see how energy efficient a model is before they buy.
    ReferencedFileTypeCode_FOOD_CONTACT_CONFORMITY_CERTIFICATE: URIRef  # The certificate of conformity for suitability for food contact is a document issued by the manufacturer or the person placing the product on the European market. It certifies that the product sold complies with the EC Regulation 1935/2004. Thus, it is proven to be safe to get in contact with food.
    ReferencedFileTypeCode_GROUP_CHARACTERISTIC_SHEET: URIRef
    ReferencedFileTypeCode_HAZARDOUS_SUBSTANCES_DATA: URIRef  # Link to a file where to locate the 'out of network data' additional data concerning the control of substances can be found.
    ReferencedFileTypeCode_IFU: URIRef  # Link to a file containing the (electronic) Instructions For Use (IFU or eIFU).
    ReferencedFileTypeCode_IFU_INCLUDING_CLEANING_DISINFECTION_STERILISATION_INSTRUCTIONS: URIRef  # Indicates that the instructions for cleaning/disinfecting/sterilisation are included in the IFU (Instructions For Use).
    ReferencedFileTypeCode_INGREDIENTS_LABEL: URIRef  # The Ingredients label image is a list of ingredients printed on the packaging. It may be separated by language in multiple areas on the product.
    ReferencedFileTypeCode_INTERNAL_VIEW: URIRef  # The picture of the inside of a trade item mainly used for non food products (e.g., The inside of a refrigerator or the inside of a suitcase.
    ReferencedFileTypeCode_LIGHTING_FACT_LABEL: URIRef  # Link to a file containing a visual representation of the product label containing information related to the light characteristics of the product. The lighting facts label makes it easy to compare bulb characteristics such as brightness, colour, life, and estimated operating cost for the year.
    ReferencedFileTypeCode_LOGO: URIRef  # Link to a file containing the Manufacturer or Brand Logo(s) associated with the product.
    ReferencedFileTypeCode_MARKETING_INFORMATION: URIRef  # Link to a file with product information associated with selling a product or service.
    ReferencedFileTypeCode_MATERIAL_SAMPLES: URIRef  # URL to website, images that the potential material, swatches, finishes the trade item might be available in.
    ReferencedFileTypeCode_MOBILE_DEVICE_IMAGE: URIRef  # Trade Item image that represents the image the manufacturer supplies to the consumer for mobile device applications. This would be a pack shot or image of the trade item that may be optimised for digital mobile display or added elements to help consumer recoginise the product. This should not be used as the Mobile Ready Hero Image. Some regulations require an actual image of the product and do not allow Mobile Ready Hero Images.
    ReferencedFileTypeCode_MOBILE_READY_HERO_IMAGE: URIRef  # A Mobile Ready Hero Image (MRHI) is a representation of a real world product that may differ from a standard pack shot, but that maintains the majority of the physical pack's key elements of design, shape and colour, and is therefore recognisable on a digital shelf. In addition the image should contain elements of The 4 Ws: Who is the brand, What it is, Which variety it is and how much. The Mobile Ready Hero Image (MRHI) is specified in the GS1 Mobile Ready Hero Image Guideline https://www.gs1.org/standards/Mobile-Ready-Hero-Image
    ReferencedFileTypeCode_MONTAGE_IMAGE: URIRef  # A Montage is the physical over layering of distinct images to create a final digital image. This process allows for a composite to be created with the future possibility of reconstruction without having to return to studio for correction, should an element be added or removed.
    ReferencedFileTypeCode_NUTRITION_FACT_LABEL: URIRef  # Link to a file containing a visual representation of the product label containing the nutritional information.
    ReferencedFileTypeCode_NUTRITION_FACT_LABEL_WITH_INGREDIENTS: URIRef  # Link to a file containing a visual representation of the product label containing the nutritional information with the inclusion of the ingredient statement.
    ReferencedFileTypeCode_OPTIMISED_HERO_IMAGE: URIRef  # An Optimised Hero Image type is to support retail, consumers, distributors and foodservice operators in completing their online sites. These images will assist consumers to identify specific information about the products they are purchasing. The image is a representation of a real world product, built specifically for use on larger screens that may differ from a standard pack shot, but that maintains the majority of the physical pack's key elements of design, shape and colour, and is therefore recognisable on a digital shelf.
    ReferencedFileTypeCode_ORGANIC_CERTIFICATE: URIRef  # Link to a website or file containing an organic certificate granted to the product.
    ReferencedFileTypeCode_OTHER_EXTERNAL_INFORMATION: (
        URIRef  # Link to a file containing product information of an unspecified type.
    )
    ReferencedFileTypeCode_OUT_OF_PACKAGE_IMAGE: URIRef  # Link to an image of an item out of its packaging and, if necessary, assembled ready for use by the end user. This type of file is subject the current version of the GDSN Product Image Specification Standard.
    ReferencedFileTypeCode_PACKAGING_ARTWORK: (
        URIRef  # Design files for packaging artwork for example Adobe source files.
    )
    ReferencedFileTypeCode_PATIENT_INFORMATION_LEAFLET: URIRef  # A leaflet or brochure containing important information to patients/consumers about the product to facilitate discussion and assist with the decision-making process. Example: A leaflet on a medical device like a hip joint. Or a consumer/patient-focused leaflet that contains information on the safe and effective use of a medicines. Often known in some markets as Consumer Medicines Information sheet (CMI), Product Information Leaflet (PiL/ePIL).
    ReferencedFileTypeCode_PETFOOD_FEEDING_INSTRUCTIONS: URIRef  # Link to a file containing a visual representation of the product label containing the feeding instructions for the petfood product.
    ReferencedFileTypeCode_PLANOGRAM: URIRef  # Link to a file illustrating how and where retail products should be displayed.
    ReferencedFileTypeCode_PREPARATION_INSTRUCTIONS: URIRef  # Link to a file containing a visual representation of the product label containing the preparation instructions.
    ReferencedFileTypeCode_PRODUCT_FORMULATION_STATEMENT: URIRef  # Link to a file containing the Product Formulation Statement, in lieu of a Child Nutrition Label, as formatted according to regulations and rules of an appropriate regulatory body for the target market.
    ReferencedFileTypeCode_PRODUCT_IMAGE: (
        URIRef  # Link to a file containing a visual representation of the product.
    )
    ReferencedFileTypeCode_PRODUCT_IMAGE_FORMED: URIRef  # An image of a product that has the supporting shape/form (for example a model, mannequin, hanger) removed to give the product a 3-D look.
    ReferencedFileTypeCode_PRODUCT_LABEL_IMAGE: URIRef  # Link to a file containing a visual representation of the product label.
    ReferencedFileTypeCode_PRODUCT_WEBSITE: URIRef  # Link to a website containing product specific information. Examples of this could be a link to a website dedicated to the product or a link to the area within the manufacturer or brand owner website that contains the product information
    ReferencedFileTypeCode_QR_CODE: URIRef  # Link to a QR code URL/URI.
    ReferencedFileTypeCode_QUALITY_CONTROL_PLAN: URIRef  # Document which detailed information about the quantity of laboratory/analytical tests and the evaluated parameters.
    ReferencedFileTypeCode_RECIPE_WEBSITE: (
        URIRef  # Link to a website containing recipes associated with the product
    )
    ReferencedFileTypeCode_RECYCLABILITY_ASSESSMENT_CERTIFICATE: URIRef  # Link to a file containing the certificate for recyclability granted to the packaging of the item.
    ReferencedFileTypeCode_REGULATORY_INSPECTION_AUDIT: URIRef  # Inspection report of the inspections. For example foodstuffs, pharmaceuticals and other types of products that are regulated.
    ReferencedFileTypeCode_RISK_ANALYSIS_DOCUMENT: URIRef  # Document which describes how the supplier assured the quality control of the end products or during the production process. The process can be a supplier internal control system, a simple kind of risk analysis or systematic preventive approach according Hazard Analysis and Critical Control Points (HACCP).
    ReferencedFileTypeCode_SAFETY_DATA_SHEET: URIRef  # Link to a file containing the product's Safety Data Sheet (SDS). This file can be either an image or a document
    ReferencedFileTypeCode_SAFETY_SUMMARY_SHEET: URIRef  # A link to a summary sheet document that is available to workers to understand how to deal with chemicals in an emergency situation.
    ReferencedFileTypeCode_SAMPLE_SHIPPING_ORDER: URIRef  # Document is a sample shipping order. A sample shipping order isn't needed for every item (GTIN), but a shipping order can differ from GTIN to GTIN. E.g. in case an item is an organic product the sample shipping order needs to contain the organic product origin number according article 31 of the implementing regulations EG Nr. 889/2008. For non-organic items this information isn't needed.
    ReferencedFileTypeCode_SIDEKICK_IMAGE: URIRef  # Retail, consumers, distributors and foodservice operators complete their online transactions using their smart devices. These images may be used to inform a customer of benefits or nutritional claims of a product. This is a supplementary image or graphic, generally used to support the Hero image.
    ReferencedFileTypeCode_SOCIAL_MEDIA_IMAGE: URIRef  # Trade Item image representing the image the manufacturer is supplying to the consumer to depict the social media associated to the item. This image is being shared on the social media outlet.
    ReferencedFileTypeCode_SUMMARY_OF_PRODUCT_CHARACTERISTICS: URIRef  # Specific document required before any medicinal product or biocidal product is authorized for marketing.  Example European Commission
    ReferencedFileTypeCode_SUPPLEMENT_FACT_LABEL: URIRef  # Link to a file containing a visual representation of the product label containing information related to the supplement or nutrient product. The supplement facts label provides about what active/nutritional ingredients are used in the formula along with dosage recommendations for dietary supplements.
    ReferencedFileTypeCode_TECHNICAL_DATA_SHEET: URIRef  # The product specification sheet, created by the manufacturer, summarises the technical characteristics and other properties of the product, relating to technological and commercial purposes. Example: https://dl.gedal.fr/docsgedal/FP/3255290252425.pdf
    ReferencedFileTypeCode_TECHNICAL_DRAWING: URIRef  # A precise and detailed technical drawing of an object, as employed in industries such as engineering, construction, architecture etc. https://en.wikipedia.org/wiki/Engineering_drawing https://en.wikipedia.org/wiki/Technical_drawing
    ReferencedFileTypeCode_TESTING_METHODOLOGY_RESULTS: URIRef  # Document which contains microbiological and physico-chemical findings of the product which are observed during product testing.
    ReferencedFileTypeCode_TRADE_ITEM_DESCRIPTION: URIRef  # Identifies the reference to an external description of a Trade Item. The link (e.g. URL) to the external description. will be in the appropriate attribute
    ReferencedFileTypeCode_TRADE_ITEM_IMAGE_WITH_DIMENSIONS: URIRef  # Link to a website, file, or image containing the product's image with its dimensions. This especially important for built-in products as ovens and fridges. Ex : http://www.docstoc.com/docs/125126778/GSS-GEW-Food-Savers-Food-Storage-Containers.
    ReferencedFileTypeCode_VIDEO: URIRef  # Link to a file containing a video clip which is relevant to the product. Examples are commercials, trailers, or instructional/ how to use video files.
    ReferencedFileTypeCode_VISUAL_VERIFICATION_IMAGE: URIRef  # Link to a file containing a visual representation of the product for the purpose of visual verification. Usage may be to examine the trade item master data against the product image. Note these images might not necessarily comply with image standards and may be restricted for a visual verification usage.
    ReferencedFileTypeCode_WARRANTY_INFORMATION: URIRef  # Link to a file with information associated with any guarantee given by a company stating that a product is reliable and free from known defects and that the seller will, without charge, repair or replace defective parts within a given time limit and under certain conditions.
    ReferencedFileTypeCode_WEBSITE: (
        URIRef  # Link to a website containing product or manufacturer information.
    )
    ReferencedFileTypeCode_ZOOM_VIEW: URIRef  # A picture of a portion of a trade item (e.g., the wheels of a suitcase or the ingredients list of a food trade item).
    RelativeHumidity: URIRef  # The ratio of the partial pressure of water vapour in an an air-water mixture to the saturated vapour pressure of water at a prescribed temperature.  Typically expressed as a percentage.
    Resistance: URIRef  # The ratio of the potential difference across an electrical component to the current passing through it. It is a measure of the opposition to the flow of electric charge. The real part of the impedance, characterised by the dissipation of energy as opposed to its storage.  SI Units: ohm
    Resistivity: URIRef  # A measure of how strongly a material resists the flow of electric current. The electric field required to achieve unit current density flowing through the material.  SI Units: ohm metre
    ReturnablePackageDepositDetails: (
        URIRef  # Details of the deposit for returnable packaging for a product.
    )
    Seafood: URIRef  # Seafood Products including fish and shellfish.
    SeasonParameterCode: URIRef
    SeasonParameterCode_ALL_YEAR: URIRef  # All Year
    SeasonParameterCode_AUTUMN: URIRef  # For products that are seasonal in nature and apply to the Autumn selling season only
    SeasonParameterCode_AUTUMN_WINTER: URIRef  # For products that are seasonal in nature and apply to both the Autumn and Winter selling seasons
    SeasonParameterCode_SPRING: URIRef  # For products that are seasonal in nature and apply to the Spring selling season only
    SeasonParameterCode_SPRING_SUMMER: URIRef  # For products that are seasonal in nature and apply to both the Spring and Summer selling seasons
    SeasonParameterCode_SUMMER: URIRef  # For products that are seasonal in nature and apply to the Summer selling season only
    SeasonParameterCode_WINTER: URIRef  # For products that are seasonal in nature and apply to the Winter selling season only
    SecurityMarking: URIRef
    SecurityMarking_HOLOGRAM: URIRef  # A holographic image formed using light diffraction and interference of light waves, capable of representing a three-dimensional object or multiple images, depending on the angle of observation.
    SecurityMarking_MICROPRINTING: URIRef  # A hidden pattern that is too small to read easily without means of optical magnification such as a microscope
    SecurityMarking_UVINK: URIRef  # A hidden pattern or marking that is invisible when observed under normal visible light but which fluoresces when observed using ultra-violet light
    SecurityMarking_WATERMARK: URIRef  # A conventional watermark in which a pattern within a translucent sheet becomes visible when observed via transmitted light (typically due to reduced opacity of the pattern), whereas the pattern remains hidden when observed via light reflected off the surface
    SensorAlertType: URIRef  # A code list for reasons for generating a sensor alert, including an alarm condition or an error condition
    SharpnessOfCheeseCode: URIRef
    SharpnessOfCheeseCode_EXTRA_EXTRA_SHARP: URIRef
    SharpnessOfCheeseCode_EXTRA_SHARP: URIRef
    SharpnessOfCheeseCode_MILD: URIRef
    SharpnessOfCheeseCode_REGULAR: URIRef
    SharpnessOfCheeseCode_SHARP: URIRef
    SharpnessOfCheeseCode_UNCLASSIFIED: URIRef
    SizeCodeDetails: URIRef  # A grouping of properties related to the representing the size of a product, by specifying a value from a specified code list.
    SizeDetails: (
        URIRef  # A grouping of properties related to the size of a wearable product
    )
    SizeGroupCode: URIRef
    SizeGroupCode_BOYS: URIRef
    SizeGroupCode_GIRLS: URIRef
    SizeGroupCode_INFANTS: URIRef
    SizeGroupCode_JUNIORS: URIRef
    SizeGroupCode_MATERNITY: URIRef
    SizeGroupCode_MENS: URIRef
    SizeGroupCode_MENS_TALL: URIRef
    SizeGroupCode_MISSES: URIRef
    SizeGroupCode_PETITE: URIRef
    SizeGroupCode_WOMENS: URIRef
    SizeGroupCode_WOMENS_TALL: URIRef
    SizeSystemCode: URIRef
    SizeSystemCode_AUSTRALIA: URIRef
    SizeSystemCode_CONTINENTAL: URIRef
    SizeSystemCode_EUROPE: URIRef
    SizeSystemCode_JAPAN: URIRef
    SizeSystemCode_MEXICO: URIRef
    SizeSystemCode_UK: URIRef
    SizeSystemCode_US: URIRef
    SizeTypeCode: URIRef
    SizeTypeCode_BACK: URIRef
    SizeTypeCode_CHEST_BUST: (
        URIRef  # The measurement around the widest part of the chest/bust.
    )
    SizeTypeCode_COLLAR: URIRef
    SizeTypeCode_CUP: URIRef
    SizeTypeCode_HIPS: URIRef  # The measurement around the fullest part of the hips.
    SizeTypeCode_INSEAM: URIRef
    SizeTypeCode_LENGTH: URIRef
    SizeTypeCode_ONE_DIMENSION: URIRef
    SizeTypeCode_OUTSIDE_LEG: URIRef  # The measurement of the outside leg seam. This is the distance from the waist to the bottom of the trousers.
    SizeTypeCode_SLEEVE: URIRef
    SizeTypeCode_WAIST: URIRef
    SizeTypeCode_WIDTH: URIRef
    SolidAngle: URIRef  # A three-dimensional equivalent to planar angle, indicating a measure of the field of view subtended by an object when viewed from a specified point, the apex.  The solid angle is the surface area subtended at radius r from the apex divided by the square of that radius r.    SI Units: steradian etc.
    SourceAnimalCode: URIRef
    SourceAnimalCode_ALLIGATOR: (
        URIRef  # A crocodilian in the genus Alligator of the family Alligatoridae.
    )
    SourceAnimalCode_ASS: URIRef  # A domesticated member of the horse family.
    SourceAnimalCode_BEAR: URIRef  # Mammals of the family Ursidae.
    SourceAnimalCode_BEEF_COW: URIRef  # Cattle raised principally for meat production, other uses include leather and products used in shampoo and cosmetics.
    SourceAnimalCode_BOAR: URIRef  # A wild relative of the domestic pig.
    SourceAnimalCode_BUFFALO: (
        URIRef  # A large bovine animal, frequently used as livestock.
    )
    SourceAnimalCode_CALF: URIRef  # A general term for a juvenile member of any species of domestic cattle which is intentionally raised to be processed at a young age.
    SourceAnimalCode_CAMEL: URIRef  # Even-toed ungulates within the genus Camelus.
    SourceAnimalCode_CHICKEN: URIRef  # A domesticated fowl.
    SourceAnimalCode_COCKEREL: URIRef  # A male chicken.
    SourceAnimalCode_COW: URIRef  # A domesticated member of the subfamily Bovinae.
    SourceAnimalCode_CROCODILE: (
        URIRef  # Any species belonging to the family Crocodylidae.
    )
    SourceAnimalCode_DEER: URIRef  # Ruminant mammals forming the family Cervidae.
    SourceAnimalCode_DOG: URIRef  # A domesticated form of the Wolf, a member of the Canidae family of the order Carnivora.
    SourceAnimalCode_DUCK: URIRef  # Aquatic birds, mostly smaller than the swans and geese, and may be found in both fresh water and sea water.
    SourceAnimalCode_DUCKLING: URIRef  # A young duck.
    SourceAnimalCode_FISH: URIRef  # Fresh or sea water fish.
    SourceAnimalCode_FOWL: URIRef  # Non-domesticated birds in general but usually refers to birds belonging to one of two biological orders, namely the gamefowl or landfowl and the waterfowl.
    SourceAnimalCode_FROG: URIRef  # Amphibians in the order Anura.
    SourceAnimalCode_GOAT: (
        URIRef  # A member of the Bovidae family and is closely related to the sheep.
    )
    SourceAnimalCode_GOOSE: URIRef  # A bird belonging to the family Anatidae
    SourceAnimalCode_GROUSE: URIRef  # A group of birds from the order Galliformes.
    SourceAnimalCode_GUINEAFOWL: URIRef  # A family of birds in the Galliformes order
    SourceAnimalCode_HARE: URIRef  # Leporidaes belonging to the genus Lepus.
    SourceAnimalCode_HORSE: URIRef  # a hoofed (ungulate) mammal, a subspecies of one of seven extant species of the family Equidae.
    SourceAnimalCode_INVERTEBRATE: URIRef  # Fresh or sea water invertebrate.
    SourceAnimalCode_LAMB: URIRef  # A young domestic sheep.
    SourceAnimalCode_LAND_SNAIL: URIRef  # A member of the molluscan class Gastropoda that have coiled shells in the adult stage and live on land.
    SourceAnimalCode_MILK_COW: URIRef  # Also referred to Milk Cattle, this cow is bred to produce large quantities of Milk, from which dairy products are made.
    SourceAnimalCode_MOOSE: URIRef  # The largest extant species in the deer family.
    SourceAnimalCode_OSTRICH: URIRef  # Large flightless bird native to Africa.
    SourceAnimalCode_OTHER: URIRef  # Other animal not specified on this list.
    SourceAnimalCode_PARTRIDGE: URIRef  # Medium-sized birds, intermediate between the larger pheasants and the smaller quails.
    SourceAnimalCode_PHEASANT: (
        URIRef  # A bird in the subfamily of Phasianidae in the order Galliformes.
    )
    SourceAnimalCode_PIGEON: URIRef  # A bird in the family Columbidae.
    SourceAnimalCode_PORK: URIRef  # Meat from the domestic pig
    SourceAnimalCode_POUSSIN: (
        URIRef  # A young chicken, less than 28 days old at slaughter
    )
    SourceAnimalCode_QUAIL: (
        URIRef  # Several genus of mid-sized birds in the pheasant family.
    )
    SourceAnimalCode_RABBIT: (
        URIRef  # Small mammals in the family Leporidae of the order Lagomorpha
    )
    SourceAnimalCode_RAT: URIRef  # Rats are various medium-sized, long-tailed rodents of the superfamily Muroidea.
    SourceAnimalCode_REINDEER: URIRef  # An Arctic and Subarctic-dwelling deer, widespread and numerous across the Arctic and Subarctic.
    SourceAnimalCode_ROE_DEER: (
        URIRef  # A deer species of Europe, Asia Minor, and Caspian coastal regions.
    )
    SourceAnimalCode_SHEEP: URIRef  # Small ruminants, usually with a crimped hair called wool and often with horns forming a lateral spiral.
    SourceAnimalCode_SHELLFISH: URIRef  # A fresh or sea water animal, such as a mollusk or crustacean, that has a shell or shell-like exoskeleton.
    SourceAnimalCode_SNAKE: (
        URIRef  # Elongate legless carnivorous reptiles of the suborder Serpentes.
    )
    SourceAnimalCode_SNIPE: URIRef  # Any of nearly 20 wading bird species in three genera in the family Scolopacidae.
    SourceAnimalCode_SPARROW: URIRef  # Small passerine birds in the family Passeridae.
    SourceAnimalCode_THRUSH: (
        URIRef  # Plump, soft-plumaged, small to medium-sized passerine birds.
    )
    SourceAnimalCode_TURKEY: URIRef  # A large bird in the genus Meleagris.
    SourceAnimalCode_TURTLE: URIRef  # Reptiles characterised by a special bony or cartilaginous shell developed from their ribs that acts as a shield.
    SourceAnimalCode_WOODCOCK: URIRef  # The woodcocks are a group of seven or eight very similar living species of wading birds in the genus Scolopax.
    SourceAnimalCode_YAK: URIRef  # A long-haired bovine found throughout the Himalayan region of south Central Asia, the Tibetan Plateau and as far north as Mongolia.
    SpecificVolume: URIRef  # The volume of a substance per unit mass. The reciprocal of density.  SI Units: cubic metres per kilogram
    Speed: URIRef  # The ratio of the linear distance travelled by a body to the time taken. Speed is a scalar quantity. Velocity is a vector with magnitude and direction.  SI Units: metre per second
    SportingActivityTypeCode: URIRef
    SportingActivityTypeCode_AMERICAN_FOOTBALL: URIRef
    SportingActivityTypeCode_ARCHERY: URIRef
    SportingActivityTypeCode_BADMINTON: URIRef
    SportingActivityTypeCode_BASEBALL: URIRef
    SportingActivityTypeCode_BASKETBALL: URIRef
    SportingActivityTypeCode_BOXING: URIRef
    SportingActivityTypeCode_CLIMBING: URIRef
    SportingActivityTypeCode_CRICKET: URIRef
    SportingActivityTypeCode_CYCLING: URIRef
    SportingActivityTypeCode_DIVING: URIRef
    SportingActivityTypeCode_EQUESTRIAN: URIRef
    SportingActivityTypeCode_FENCING: URIRef
    SportingActivityTypeCode_FISHING: URIRef
    SportingActivityTypeCode_FOOTBALL: URIRef
    SportingActivityTypeCode_GOLF: URIRef
    SportingActivityTypeCode_GYMNASTICS: URIRef
    SportingActivityTypeCode_HOCKEY: URIRef
    SportingActivityTypeCode_ICE_HOCKEY: URIRef
    SportingActivityTypeCode_ICE_SKATING: URIRef
    SportingActivityTypeCode_MOTOR_CYCLING: URIRef
    SportingActivityTypeCode_RUGBY: URIRef
    SportingActivityTypeCode_RUNNING: URIRef
    SportingActivityTypeCode_SKIING: URIRef
    SportingActivityTypeCode_SQUASH: URIRef
    SportingActivityTypeCode_SURFING: URIRef
    SportingActivityTypeCode_SWIMMING: URIRef
    SportingActivityTypeCode_TENNIS: URIRef
    SportingActivityTypeCode_UNCLASSIFIED: URIRef
    SportingActivityTypeCode_UNIDENTIFIED: URIRef
    StatusType: URIRef
    StatusType_ACTIVE: URIRef  # Designation stating that an organisation/party or location is operating. Note that this is independent of whether or not the GLN is active.
    StatusType_INACTIVE: URIRef  # Designation stating that an organisation/party or location is not operating. Note that this is independent of whether or not the GLN is inactive.
    SurfaceDensity: URIRef  # The mass per unit area distributed over a surface.  SI Units: kilogram per square metre
    SurfaceTension: URIRef  # The attractive force exerted upon the surface molecules of a liquid by the molecules beneath that tends to draw the surface molecules into the bulk of the liquid and makes the liquid assume the shape having the minimum surface area.  SI Units: newton per metre
    TargetConsumerGenderCode: URIRef
    TargetConsumerGenderCode_FEMALE: URIRef
    TargetConsumerGenderCode_MALE: URIRef
    TargetConsumerGenderCode_UNISEX: URIRef
    TargetMarketDetails: URIRef  # A set of target market details (product release date and associated countries) for the product.
    Temperature: URIRef  # A measure of whether two systems are relatively hot or cold with respect to one another; two systems brought into contact will eventually reach thermal equilibrium and reach the same temperature as thermal energy (heat) flows from the system with higher temperature to the system with lower temperature.  SI Units: kelvin
    TextileMaterialDetails: URIRef  # Details on the composition of any materials used to make a product using textiles.
    Time: URIRef  # A dimension that enables distinction between two otherwise identical events that occur at the same point in space. The interval between such events is the basis of time measurement.  SI Units: second
    Torque: URIRef  # The product of a force and its perpendicular distance from a point about which it causes rotation or torsion.  SI Units: newton metre
    TradeChannelCode: URIRef
    TradeChannelCode_INSTORE_ONLY: URIRef  # Offer avalilable only in stores.
    TradeChannelCode_OMNICHANNEL: URIRef  # Offer avalilable both in stores and online.
    TradeChannelCode_ONLINE_ONLY: URIRef  # Offer avalilable online only.
    TypeCode: URIRef  # A code list.
    UpperTypeCode: URIRef
    UpperTypeCode_CLOSED_TOE_CLOSED_BACK_OPEN_INSTEP: URIRef
    UpperTypeCode_CLOSED_TOE_OPEN_BACK: URIRef
    UpperTypeCode_CLOSED_TOE_STRAP_BACK: URIRef
    UpperTypeCode_FULLY_CLOSED: URIRef
    UpperTypeCode_OPEN_TOE_FULLY_CLOSED_BACK: URIRef
    UpperTypeCode_OPEN_TOE_OPEN_BACK: URIRef
    UpperTypeCode_OPEN_TOE_STRAP_BACK: URIRef
    UpperTypeCode_UNCLASSIFIED: URIRef
    Voltage: URIRef  # The value of an electromotive force or electrostatic potential difference, expressed in volts.  SI Units: volt
    Volume: URIRef  # The amount of three-dimensional space occupied by a body, measured in cubic length units.  SI Units: cubic metre
    VolumeFlowRate: URIRef  # The volume of fluid that passes per unit of time.  SI Units: cubic metre per second
    VolumeFraction: URIRef  # The dimensionless ratio of a volume of one substance to the volume of solid, liquid or gas in which it is contained.  Typical units: parts per million, parts per billion, etc.
    VolumetricFlux: URIRef  # The volume of fluid that passes per unit of time per unit area perpendicular to the flow direction.  SI Units: cubic metre per second per square metre
    WarrantyPromise: URIRef  # An assurance that the product is reliable and that repairs or replacement will be done free of charge within a given time limit and under certain conditions in the event of a defect.
    Wavenumber: (
        URIRef  # The number of waves per unit length.  SI Units: reciprocal metre
    )
    WearableProduct: URIRef  # Products that are worn on the body.
    acceptedPaymentMethod: URIRef  # Code indicating a means of payment, for example, BANK_CHEQUE, CASH, etc.
    activityIdeas: URIRef  # A link to ideas for using a product or engaging in other forms of entertainment, particularly with children.
    additionalLocationID: URIRef  # Location identifiers assigned and managed by government bodies, trade organisations, and other entities.
    additionalOrganizationID: URIRef  # Party/organisation identifiers assigned and managed by government bodies, trade organisations, and other entities.
    additionalOrganizationIdentificationTypeValue: URIRef  # The value associated with the Additional Organization Identification Type Value.
    additionalProductClassification: (
        URIRef  # Relates to a set of additional product classification details
    )
    additionalProductClassificationCode: (
        URIRef  # Code specifying the applied additional product classification scheme.
    )
    additionalProductClassificationCodeDescription: URIRef  # A description related to  the additional product classification code value.
    additionalProductClassificationValue: URIRef  # Code specifying an additional product classification other than the GS1 Global Product Classification. The applied classification scheme is specified as additional information together with the classification value.
    additionalProductDescription: URIRef  # Additional variants necessary to communicate to the industry to help define the product. Multiple variants can be established for each GTIN for e.g. Style, Colour, and Fragrance .
    additive: (
        URIRef  # Relates to details about any additives that a product may contain.
    )
    additiveLevelOfContainment: (
        URIRef  # Code indicating the level of presence of the additive.
    )
    additiveName: URIRef  # The name of any additive or genetic modification contained or not contained in the product .
    address: URIRef  # The postal address for an organization or place.
    addressCountry: URIRef  # Code specifying the country (and country subdivision) for the address using ISO 3166-1.
    addressLocality: (
        URIRef  # Text specifying the name of the locality, for example a city.
    )
    addressRegion: URIRef  # Text specifying a province or state in abbreviated format for example NJ.
    addressSuburb: URIRef  # A suburb within a town or city.
    afterHoursContact: URIRef  # Links to after-hours contact information. For general contact details, gs1:contactPoint SHALL be used.
    alcoholicBeverageSubregion: URIRef  # A legally defined geographical region where the grapes for a wine were grown also known as an appellation. It is recommended to populate this property with an ISO 3166-2 code to indicate country and subdivision.
    allergenInfo: URIRef  # A link to a description of the allergen information.
    allergenLevelOfContainmentCode: (
        URIRef  # Code specifying the level of presence of the allergen.
    )
    allergenSpecificationAgency: URIRef  # The agency or other organization that defines or manages the criteria for allergen containment.
    allergenSpecificationName: URIRef  # Free text field containing the name and version of the regulation or standard that defines the criteria of allergen containment.
    allergenStatement: URIRef  # Textual description of the presence or absence of allergens as governed by local rules and regulations, specified as one string.
    allergenType: URIRef  # Code specifying the type of allergen.
    anatomicalForm: URIRef  # Describes the meat product in terms of whether it is the whole animal or part of the animal which has been cut such as the muscle, bone, organ, or fat.
    appDownload: URIRef  # A link to a related mobile app
    applicableTo: URIRef  # A property linking a gs1:linkType to the primary GS1 key(s) for which it can be used. Similar to rdfs:Domain but the value space is a GS1 Application Identifier, not a class.
    audioFile: URIRef  # Link to a file containing an audio clip which is relevant to the product. Examples are commercials, or instructional/ how to use audio files.
    authenticity: URIRef  # Links to details of covert/overt security markings that may be used to check authenticity of a product instance.
    authenticitySecurityFeatureInstructions: URIRef  # Provides human-readable instructions about how to locate a physical security marking and read a value from it.
    authenticitySecurityFeatureInstructionsURL: URIRef  # Links to online instructions about how to locate a physical security marking and read a value from it.
    authenticitySecurityFeatureRegularExpression: URIRef  # Links to a regular expression to be used to perform syntax validation (plausibility checking) of a string value read from a physical security marking.
    authenticitySecurityFeatureType: URIRef  # Links to a URI code value indicating a particular type of physical security marking.
    authenticitySecurityFeatureValue: (
        URIRef  # Links to a string value read from a physical security marking.
    )
    availabilityEnds: URIRef  # The date from which the product is no longer available from the information provider, including seasonal or temporary product and services .
    availabilityStarts: URIRef  # The date from which the product is available from the information provider, including seasonal or temporary product and services.
    availableAtOrFrom: (
        URIRef  # The location the offered product or service is available from.
    )
    availableLanguage: (
        URIRef  # ISO 639-1 code specifying the language of a specified contact point.
    )
    awardPrize: URIRef  # An award or prize given to the product.
    awardPrizeCode: URIRef  # Indicates the achievement of the product in relation to a prize or award, e.g. winner, runner-up, shortlisted.
    awardPrizeCountryCode: URIRef  # An ISO standard code identifying the country in which a prize or award is given. It is recommended to populate this property with an ISO 3166-1 country code.
    awardPrizeDescription: URIRef  # Text that describes the awards won.
    awardPrizeJury: (
        URIRef  # Free text listing members of the jury that awarded the prize.
    )
    awardPrizeName: (
        URIRef  # The name of a prize or award which the product has received.
    )
    awardPrizeYear: URIRef  # The year in which a prize or award was given.
    backgroundInfo: URIRef  # A link to information typically from the owner of the identified entity about the creative background, thought leadership or influence of the identified entity. This may include the inspiration, innovation for a development process, literary approach or, the science or technology used.
    baseLocation: URIRef  # A fixed physical location where a mobile location most commonly resides. If gs1:glnType is present, gs1:baseLocationGLN SHALL only be used when gs1:glnType is gs1:GLN_TypeCode-MOBILE_PHYSICAL_LOCATION
    bestBeforeDate: URIRef  # Best before date on the label or package signifies the end of the period under which the product will retain specific quality attributes or claims even though the product may continue to retain positive quality attributes after this date. Best before date is primarily used for consumer information and may be a regulatory requirement.
    beverageVintage: URIRef  # The year in which the majority of ingredients are harvested and/or the alcoholic beverage is produced. Determination as to whether the vintage year is the harvest date or production date is according to requirements in the Target Market.
    biotinPerNutrientBasis: URIRef  # Biotin Acid per specified nutrient basis quantity.
    bonelessClaim: URIRef  # The descriptive term that is used by the product manufacturer to identify whether the product makes a specific claim to contain no bones.
    brand: URIRef  # The brand of the product that appears on the consumer package.
    brandHomepageClinical: (
        URIRef  # A link to a brand presence aimed at clinical professionals.
    )
    brandHomepagePatient: URIRef  # A link to a brand presence aimed at patients.
    brandName: (
        URIRef  # The brand name of the product that appears on the consumer package.
    )
    brandOwner: URIRef  # The brand owner of the product. The organization that is responsible for allocating the GTIN to the product.
    calciumPerNutrientBasis: URIRef  # Calcium per specified nutrient basis quantity.
    carbohydratesPerNutrientBasis: (
        URIRef  # Carbohydrates per specified nutrient basis quantity.
    )
    careersInfo: URIRef  # A link to information about jobs, careers, or other employment opportunities associated to an organisation or location.
    catchZone: URIRef  # Free text field describing the sea zone from which the product was caught in.
    certification: (
        URIRef  # Certification information about a product, organisation or location.
    )
    certificationAgency: URIRef  # Name of the organisation issuing the certification standard or other requirement being met .
    certificationAgencyURL: URIRef  # URL of the organisation issuing the certification standard or other requirement being met. e.g. https://www.msc.org , https://www.fsc.org
    certificationAuditDate: (
        URIRef  # Date of completion of the auditing needed for certification
    )
    certificationEndDate: URIRef  # Last date of validity for the certification. (After this date the certification lapses and would need to be renewed/replaced)
    certificationIdentification: URIRef  # A reference (i.e, to a certificate instance) issued to confirm that a product, party or location has passed certification. e.g. 'XSC-C-12345'
    certificationInfo: URIRef  # A link to certification information.
    certificationStandard: URIRef  # Name of the certification standard. Free text. Example: 'Egg classification' .
    certificationStartDate: URIRef  # First date of validity for the certification
    certificationStatement: URIRef  # Certification scope statement of the individual certification instance. The same certificationStandard can be issued with different values of certificationStatement in different instances.
    certificationStatus: URIRef  # Indicates the current status of the certification, e.g. active or inactive.
    certificationSubject: URIRef  # References the object (e.g. product, asset, container), party or location being certified. If multiple values are specified, the certification details apply to the logical conjunction (AND) of groups of different types, while a logical disjunction (OR) applies within each group of the same type. For example, two sibling organisations O1 and O2 can process products P1 and P2 at locations L1 and L2: meaning that either organisation can process either product at either location (OR); but the certificate holds for the combinations of organisation (either O1 OR O2) AND product (either P1 OR P2) AND location (either L1 OR L2)
    certificationType: URIRef  # Indicates the type of certification
    certificationURI: URIRef  # If gs1:certificationURI is present, it should point to data about this individual certificate within a repository maintained by the certification agency.
    certificationValue: URIRef  # The certification's standard value. Example: '4'.
    cheeseFirmness: URIRef  # The firmness of the cheese product for example EXTRA_HARD.
    cheeseMaturationPeriodDescription: URIRef  # A descriptive way to specify a date range as some cheeses are matured over a period of time, but not an exact period. For example 3 to 4 weeks, over 1 year etc. The term maturation is also known in other markets as Aged.
    chloridePerNutrientBasis: URIRef  # Chloride per specified nutrient basis quantity.
    cholesterolPerNutrientBasis: (
        URIRef  # Cholesterol per specified nutrient basis quantity.
    )
    chromiumPerNutrientBasis: URIRef  # Chromium per specified nutrient basis quantity.
    circle: URIRef  # A circle is the circular region of a specified radius centred at a specified latitude and longitude. A circle is expressed as a pair followed by a radius in meters.
    clothingCut: URIRef  # Supplemental information to indicate the clothing cut or silhouette make of the garment. For example, silhouette details for a pair of jeans such as boot cut, or loose fit, comfort fit.
    collarType: URIRef  # A free text description of the type of collar on the garment.
    colourCode: (
        URIRef  # Relates to a set of details about the colour code for a product
    )
    colourCodeList: URIRef  # The parties controlling the colour code lists. Dependent on colour code value.
    colourCodeValue: URIRef  # A code indicating the colour of an object according to a specific code list. The applied code list is specified as additional information together with the colour code.
    colourDescription: URIRef  # A description of the colour of an object.
    consumerFirstAvailabilityDateTime: URIRef  # The first date/time that the buyer is allowed to sell the product to consumers. Usually related to a specific geography. ISO 8601 date format CCYY-MM-DDTHH:MM:SS.
    consumerHandlingStorage: URIRef  # Link to a website, file, or image containing the manufacturer's recommendations for how the consumer or end user should store and handle the product.
    consumerHandlingStorageInfo: URIRef  # A link to information about safe handling and storage for consumer use.
    consumerLifestage: URIRef  # Indicates, with reference to the product branding, labelling or packaging, the descriptive term that is used by the product manufacturer to identify the period or stage in the consumer's life during which the product is considered to be suitable.
    consumerPackageDisclaimer: URIRef  # Additional information that should be used in advertising and in displaying.
    consumerProductVariant: URIRef  # The consumer product variant may be used to distinguish one variant of a retail consumer trade item from another if the change does not require the allocation of a different Global Trade Item Number (per the GTIN Management Standard), but communication between trading partners is required to support consumers. The brand owner is responsible for assigning the consumer product variant.
    consumerSafetyInformation: (
        URIRef  # Information on consumer safety regarding the product.
    )
    consumerSalesCondition: URIRef  # A code indicating restrictions imposed on the product regarding how it can be sold to the consumer for example Prescription Required.
    consumerStorageInstructions: URIRef  # Expresses in text the consumer storage instructions of a product which are normally held on the label or accompanying the product. This information may or may not be labelled on the pack.
    consumerUsageInstructions: URIRef  # Free text containing the usage instructions of a product, which are normally held on the label or accompanying the product. This information may or may not be labelled on the pack.
    contactPoint: URIRef  # Contact information. To specify a contact specifically designated for after-hours support, see gs1:afterHoursContact
    contactTitle: (
        URIRef  # The job title of the person that can be contacted for example Manager.
    )
    contactType: (
        URIRef  # The function or role of a contact for example Customer Support.
    )
    containedInPlace: URIRef  # Designates the larger physical location a sub-location is located within. To specify sub-locations of a physical location, see gs1:containsPlace.
    containsPlace: URIRef  # Designates a sub-location (e.g., floor, room, shelf) within the physical location being identified. There may be multiple sub-locations associated to a single, physical location. To specify the larger physical location the sub-location is located within, see gs1:containedInPlace
    convenienceLevelPercent: URIRef  # An indication of the ease of preparation for semi-prepared products. The convenience level indicates the level of preparation in percentage required to prepare and helps the consumer to assess how long it will take to prepare the meal.
    coordinateReferenceSystem: URIRef  # Open standard spatial reference systems or coordinate reference systems that provide coordinate-based local, regional or global system used to locate geographical entities.  Values should be URIs already defined by the IOPG Geomatics Committee (https://epsg.org/), such as https://epsg.io/4326 (WGS84); https://epsg.io/4267 (NAD27); https://epsg.io/4230 (ED50); https://epsg.io/4618 (SAD69); https://epsg.io/4269 (NAD83).  For elevation values, gs1:elevation SHALL be used.
    copperPerNutrientBasis: URIRef  # Copper per specified nutrient basis quantity.
    countryCode: URIRef  # Code specifying the country for the address using ISO 3166-1.
    countryOfAssembly: URIRef  # The place where product is assembled.
    countryOfLastProcessing: URIRef  # The place where the product or ingredient was last processed and tested before importation.
    countryOfOrigin: URIRef  # Code indicating the country of origin of the product.
    countryOfOriginStatement: URIRef  # A description of the geographic area the item may have originated from or has been processed.
    countrySubdivisionCode: URIRef  # A short text string code (see values defined in ISO 3166_2) specifying the country subdivision in which an activity is performed, for example processing, bottling, manufacturing.
    countyCode: URIRef  # A code that identifies a county. A county is a territorial division in some countries, forming the chief unit of local administration. In the US, a county is a political and administrative division of a state.
    crossStreet: URIRef  # A street intersecting a main street (usually at right angles) and continuing on both sides of it.
    customerSupportCentre: URIRef  # The organization which provides product support to the trading partner organization to which merchandise is sold.
    dailyValueIntakePercent: URIRef  # The percentage of the recommended daily intake of a nutrient as recommended by authorities of the target market. Is expressed relative to the serving size and base daily value intake.
    defaultLink: URIRef  # The default link for a given identified item to which a resolver will redirect unless there is information in the request that is a better match.
    defaultLinkMulti: URIRef  # A set of 'default links' that may be differentiated by information in the HTTP request headers sent to a resolver to enable a better match than the single default link.
    department: URIRef  # The name of a division of an organization dealing with a specific activity
    dependentProprietaryProduct: URIRef  # Dependent products are products which are required to make the current product functional.
    descriptiveSize: URIRef  # An alphanumeric size factor the brand owner wishes to communicate to the consumer. IE Jumbo, Capri, Full Length, Maxi.
    dietCode: URIRef  # Links to multiple pairs of gs1:DietTypeCode and diet type sub code (free-form text string).
    dietType: (
        URIRef  # Code indicating the diet the product is suitable for example Kosher.
    )
    dietTypeDescription: (
        URIRef  # Free text for indication of diet not stated in the list of diets.
    )
    dietTypeSubcode: URIRef  # Indicates a set of agreements or a certificate name that guarantees the product is permitted in a particular diet. A diet type subcode is a subclassification of a specific diet type. For example, Pareve is a diet type subcode of Kosher.
    digitalAddress: URIRef  # The location reference associated to a digital place. If gs1:glnType is present, SHALL only be associated if the value of gs1:glnType is gs1:GLN_TypeCode-DIGITAL_LOCATION.
    digitalLocationName: URIRef  # The name of a digital place. To specify the name of a physical location, see gs1:physicalLocationName.
    discountRepeatsPerMultipleMinimum: URIRef  # If specified and set to true, the discount is available for each time the minimum qualifying criteria are met.  This can be used to express '$10 off each $50 spend', which is distinct from a 20% discount because it is quantized in units of spending.
    discountType: URIRef  # A code that specifies the type of payment discount applicable to an offer, for example BOGO.
    drainedWeight: URIRef  # The weight of the product when drained of its liquid. For example 225 GRM, Jar of pickles in vinegar.
    dueDate: URIRef  # The date by which an invoice should be paid. This data element represents an attribute of a payment slip reference number, AI (8020), and a Global Location Number (GLN) of the invoicing party.
    durationOfWarranty: URIRef  # The time period that the warranty is valid within.
    dutyFeeTaxAmount: URIRef  # The current tax or duty or fee amount applicable to the product, expressed as a floating-point numeric value that is qualified by the corresponding currency. See also gs1:priceCurrency.
    dutyFeeTaxDescription: (
        URIRef  # A description of tax type for example Taxes sure les supports audio.
    )
    dutyFeeTaxRate: (
        URIRef  # The current tax or duty rate percentage applicable to the product.
    )
    eifu: URIRef  # A link to electronic Instruction For Use instructions for Medical Devices.
    elevation: URIRef  # The elevation of a location (WGS 84). Values may be of the form 'NUMBER UNITOFMEASUREMENT' (e.g., '1,000 m', '3,200 ft') while numbers alone SHALL be a value in meters.
    eligibleQuantity: URIRef  # The quantity including unit of measure for which the offer for good or service is valid.  If this is not specified, an eligible quantity of 1 should be assumed.
    eligibleQuantityMaximum: URIRef  # The maximum quantity including unit of measure for which the offer for good or service is valid.
    eligibleQuantityMinimum: URIRef  # The minimum quantity including unit of measure for which the offer for good or service is valid.
    eligibleTradeChannel: URIRef  # A code determining the location where a user can redeem the offer, for example ONLINE_ONLY.
    email: URIRef  # Creating/sending/receiving of unstructured free text messages or documents using computer network, a mini-computer or an attached modem and regular telephone line or other electronic transmission media.
    energyFromFatPerNutrientBasis: (
        URIRef  # Energy from Fat per specified nutrient basis quantity.
    )
    energyPerNutrientBasis: URIRef  # Energy Per specified nutrient basis quantity.
    epcis: URIRef  # A link to an EPCIS repository of visibility event data.
    epil: URIRef  # A link to an electronic patient information leaflet.
    equivalentProduct: URIRef  # A product which can be substituted for the product based on supplier-defined functional equivalence to the product.
    eventsInfo: URIRef  # A link to event details.  For a page specifically for scheduling a reservation or booking an appointment, see gs1:scheduleTime.
    exactDiscountAmount: URIRef  # Links to a gs1:PriceSpecification that indicates in terms of an amount and specified currency, the exact discount on the sales price associated with a particular gs1:Discount. This property can be used to express '$10 off'.
    exactDiscountPercentage: URIRef  # A floating-point value indicating an exact percentage discount on the sales price associated with a particular gs1:Discount.  This property can be used to express '15% discount'.
    exclusionDescription: URIRef  # A text description of any products, brands, or categories that cannot be used with the offer
    expirationDate: URIRef  # The expiration date is the date that determines the limit of consumption or use of a product/coupon. Its meaning is determined based on the trade item context (e.g., for food, the date will indicate the possibility of a direct health risk resulting from use of the product after the date, for pharmaceutical products, it will indicate the possibility of an indirect health risk resulting from the ineffectiveness of the product after the date). It is often referred to as 'use by date' or 'maximum durability date'.
    expirationDateTime: URIRef  # The manufacturer determines the expiration date and time, which is relevant only for short duration and for items that will not be sent on long distances and not outside of the time zone. A typical application of AI (7003) is in hospitals or public pharmacies for special, customised, products which may have a 'life duration' shorter than one single day. The life duration varies according the pharmaceutical substances used in the treatment. The precise expiration date and time is defined at the end of the manufacturing process, and can be barcoded on the product label as an attribute to the item's GTIN. Where there is no business requirement to express the expiration date to the nearest hour (or less), AI (17) Expiration date should be used.
    faqs: URIRef  # A link to a set of frequently asked questions.
    fatInMilkContent: (
        URIRef  # The percentage of fat contained in milk content of the product.
    )
    fatPerNutrientBasis: URIRef  # Fat per specified nutrient basis quantity.
    fatpercentageInDryMatter: URIRef  # The amount of fat contained in the base product expressed in percentage.
    faxNumber: URIRef  # A fax number used for transmitting and reproducing fixed graphic material over telephone lines or other electronic transmission media.
    fibrePerNutrientBasis: URIRef  # Fibre per specified nutrient basis quantity.
    fileLanguageCode: URIRef  # The specified language to which the digital asset is targeted. It is recommended to use the ISO 639-1 language code.
    filePixelHeight: (
        URIRef  # The number of pixels along the vertical axis of the image.
    )
    filePixelWidth: (
        URIRef  # The number of pixels along the horizontal axis of the image.
    )
    firstFreezeDate: URIRef  # The first freeze date is applicable to products that are frozen directly after slaughtering, harvesting, catching or after initial processing of the product. Examples include fresh meat, meat products or fishery products. The first freeze date is determined by the organisation conducting the freezing.
    fishType: URIRef  # The type of fish for example Sea bass.
    fluoridePerNutrientBasis: URIRef  # Fluoride per specified nutrient basis quantity.
    folicAcidPerNutrientBasis: (
        URIRef  # Folic Acid per specified nutrient basis quantity.
    )
    foodBeverageRefrigerationClaim: (
        URIRef  # Identifies whether or not the product requires refrigeration.
    )
    foodBeverageTargetUse: URIRef  # The type of meal the food or beverage product is targeted to for example Breakfast.
    footwearFasteningType: URIRef  # Something that mechanically joins or affixes two or more parts together in a footwear product for example a shoe lace.
    footwearUpperType: URIRef  # The descriptive term that is used by the product manufacturer to identify whether the footwear upper is open or closed. Otherwise known as Open or Closed Upper.
    freshOrSeawaterFarmed: URIRef  # A code determining whether the fish originated from the sea or was farmed.
    functionalName: URIRef  # Describes use of the product or service by the consumer. Should help clarify the product classification associated with the GTIN.
    geneticallyModifiedDeclaration: URIRef  # A statement of the presence or absence of genetically modified protein or DNA.
    geo: URIRef  # Links to information about geocoordinates or geoshapes for a place.
    glnType: URIRef  # Indicates what type of thing is being identified by a GLN.
    globalLocationNumber: URIRef  # A Global Location Number (GLN) is the GS1 Identification Key used to identify physical locations or parties. The key comprises a GS1 Company Prefix, Location Reference and Check Digit. For more information see https://www.gs1.org/gln.
    gpcCategoryCode: URIRef  # 8-digit code (GPC Brick Value) specifying a product category according to the GS1 Global Product Classification (GPC) standard. For more information see https://www.gs1.org/gpc
    gpcCategoryDescription: URIRef  # A description of the code specifying a product category according to the GS1 Global Product Classification (GPC) standard.
    grossArea: URIRef  # The overall area of the item including packaging. This can be given using a number of different AI ranges that depend on the units in which the area is measured.
    grossVolume: URIRef  # The overall volume of the item including packaging. This can be given using a number of different AI ranges that depend on the units in which the volume is measured.
    grossWeight: URIRef  # Used to identify the gross weight of the product. The gross weight includes all packaging materials of the product. At pallet level the productGrossWeight includes the weight of the pallet itself. For example, 200 GRM, value - total pounds, total grams, etc.
    growingMethod: (
        URIRef  # The process through which fresh produce is grown and cultivated.
    )
    gtin: URIRef  # A Global Trade Item Number (GTIN) is the 14 digit GS1 Identification Key used to identify products. The key comprises a GS1 Company Prefix followed by an Item Reference Number and a Check Digit. See https://www.gs1.org/gtin  for more details.
    handledBy: URIRef  # Used when one resolver redirects all request URIs that match a given pattern without further processing, such as from GS1 to a brand-operated service. See section 7.7.1 of the Digital Link standard, version 1.1.
    harvestDate: URIRef  # The harvest date. For example, the harvest date can be the date when an animal was slaughtered or killed, a fish has been harvested, or a crop was harvested. This date  is determined by the organisation conducting the harvesting. Different organisations may use more specific terminology when referring to their specific needs and use terms such as: Date of catch or slaughter date.
    harvestDateEnd: URIRef  # The harvest end date. For example, the harvest end date can be the date when an animal was slaughtered or killed, a fish has been harvested, or a crop was harvested. This end date is determined by the organisation conducting the harvesting. Different organisations may use more specific terminology when referring to their specific needs and use terms such as: Date of catch or slaughter date. When referring to animals the date range refers to the whole animal and all meat or fish cuts derived from this animal.
    harvestDateStart: URIRef  # The harvest start date. For example, the harvest start date can be the date when an animal was slaughtered or killed, a fish has been harvested, or a crop was harvested. This start date is determined by the organisation conducting the harvesting. Different organisations may use more specific terminology when referring to their specific needs and use terms such as: Date of catch or slaughter date. When referring to animals the date range refers to the whole animal and all meat or fish cuts derived from this animal.
    hasAllergen: URIRef  # Relates to details about allergens
    hasBatchLotNumber: URIRef  # The batch or lot number associates an item with information the manufacturer considers relevant for traceability of the trade item to which the element string is applied. The data may refer to the trade item itself or to items contained. The number may be, for example, a production lot number, a shift number, a machine number, a time, or an internal production code. In cases where the same product is manufactured in different locations the brand owner and the manufacturer are responsible for ensuring the non-duplication of batch/lot numbers for a GTIN. For the re-use of batch/lot numbers with a GTIN, sector-specific constraints need to be considered.
    hasPrimaryLocation: URIRef  # Links to the place(s) that this organisation designates as their primary location(s).
    hasRetailers: URIRef  # A link to a list of retailers.
    hasReturnablePackageDeposit: URIRef  # links to details of amounts refunded for returnable package in a specified region.
    hasSerialNumber: URIRef  # A serial number is assigned to an entity for its lifetime. When combined with a GTIN, a serial number uniquely identifies an individual item. The serial number field is alphanumeric and may include all characters contained in figure 7.11-1. The brand owner and the manufacturer are responsible for ensuring the non-duplication of serial numbers for a GTIN. For the re-use of serial numbers with a GTIN, sector-specific constraints need to be considered.
    hasThirdPartyControlledSerialNumber: URIRef  # This identifier is assigned to an entity for its lifetime. When combined with a GTIN, a TPX uniquely identifies an individual item and forms a unit pack Unique Identifier (upUI) for tobacco traceability per EU 2018/574. The serial number field is alphanumeric and may include all characters contained in figure 7.11-1. The Third Party determines the TPX, but the TPX shall begin with the ID Issuer Unique Identification Code (UIC), followed by GS1 UIC Extension 1, and GS1 UIC Extension 2.
    healthClaimDescription: URIRef  # A description of health claims according to regulations of the target market.
    homepage: URIRef  # A link to general information about an organisation or brand. Typically the homepage of an organisation's website. It may include links to further information such as certifications, careers, payments, reservations, etc.
    image: URIRef  # Link to a file containing a visual representation of the product.
    inPackageDepth: URIRef  # The depth of the product in its packaging, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    inPackageDiameter: URIRef  # The measurement of the diameter of the product in its package at its largest point. For example, 165 MMT.
    inPackageHeight: URIRef  # The height of the product in the package, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    inPackageWidth: URIRef  # The width of the product in the package, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    includedAccessories: URIRef  # Any included object or device not part of the core product itself but which adds to its functionality or use.
    ingredient: URIRef  # Links to information about ingredients of a specific Food/Beverage/Tobacco product.
    ingredientContentPercentage: URIRef  # Quantity of the ingredient contained in the product as a percentage of the total product ingredients. This is used in conjunction with ingredientName.
    ingredientName: URIRef  # Free text field describing an ingredient or ingredient group. Ingredients include any additives (colourings, preservatives, e-numbers, etc.) that are encompassed.
    ingredientOfConcern: URIRef  # Indicates a claim to an ingredient, considered to be a concern for regulatory or other reasons, and which is 'contained' within the product but may not need to specify the amount whether approximate, or an accurate measurement be given.
    ingredientSequence: URIRef  # Integer (1, 2, 3...) indicating the ingredient order by content percentage of the product. (major ingredient = 1, second ingredient = 2) etc.
    ingredientStatement: URIRef  # Information on the constituent ingredient make up of the product specified as one string.
    ingredientsInfo: URIRef  # A link to facts about ingredients.
    initialCertificationDate: URIRef  # The date when the certification was originally issued. May differ from the certificationStartDate of the current recertification cycle.
    instructions: URIRef  # A link to instructions, such as assembly instructions, usage tips etc.  It is not appropriate to use this link type for healthcare regulated content applications for which specific link types are available.
    instructionsForUse: URIRef  # Link to a file containing the Instructions For Use.
    iodinePerNutrientBasis: URIRef  # Iodine per specified nutrient basis quantity.
    ironPerNutrientBasis: URIRef  # Iron per specified nutrient basis quantity.
    irradiatedCode: URIRef  # Indicates if radiation has been applied to the product.
    isCarbonated: URIRef  # Used to identify whether or not a beverage product is naturally effervescent or has been made effervescent by the addition of carbon dioxide gas.
    isDecaffeinated: URIRef  # The descriptive term that is used by the product manufacturer to identify whether or not the product contains caffeine.
    isFromConcentrate: URIRef  # Used to identify whether or not the product claims to be made from a concentrated formulation.
    isHomogenised: URIRef  # A The indication whether or not the milk used was actively homogenised. The homogenisation of milk is a technical process in the dairy. The milk fat is milled to such an extent that further creaming is prevented.
    isInstant: URIRef  # Determines whether the product is instant.
    isMaternity: URIRef  # Indicates, with reference to the product branding, labelling or packaging, the descriptive term that is used by the product manufacturer to identify if the product is intended as maternity wear.
    isOnlyAvailableThroughRetailer: URIRef  # If specified and set to true, the discount is only available through the retailer making the offer.
    isOnlyWithMailingListSignup: URIRef  # If specified and set to true, the discount is only available for customers who have signed up to the retailer's mailing list.
    isOnlyWithPaymentCard: URIRef  # If specified, the discount is only available when purchasing using one of the specified payment card types.
    isOnlyWithRetailerLoyaltyCard: URIRef  # If specified and set to true, the discount is only available for holders of the retailer's own loyalty card.
    isOnlyWithRetailerPaymentCard: URIRef  # If specified and set to true, the discount is only available for holders of the retailer's own store payment card.
    isPatterned: URIRef  # The descriptive term that is used by the product manufacturer to identify whether or not the product has a patterned design.
    isPittedStoned: URIRef  # The descriptive term that is used by the product manufacturer to identify whether or not a fruit or vegetable product has been de-stoned or pitted prior to being offered for sale.
    isProductRecalled: URIRef  # An indicator for the product to determine if the Manufacturer or Supplier has recalled the product.
    isPromoterExclusiveOffer: (
        URIRef  # Determines whether the offer is only provided by the promoter
    )
    isRindEdible: URIRef  # An indicator whether or not the cheese rind is edible. Some cheeses are coated in plastic or their surface is treated with other traditional substances to increase their shelf life. This can result in the rind no longer being edible.
    isSeedless: URIRef  # Determines whether the product is seedless as grown.
    isShelledPeeled: URIRef  # The descriptive term that is used by the product manufacturer to identify whether or not the product or its contents have been shelled/peeled prior to being offered for sale.
    isSliced: URIRef  # Determines whether the product comes pre-sliced.
    isThermal: URIRef  # The descriptive term that is used to identify whether the product is thermal.
    isVintage: URIRef  # Identifies whether the product makes claim to being vintage.
    isWashedReadyToEat: (
        URIRef  # Determines whether product has been prewashed and is ready to eat.
    )
    isWaterproof: URIRef  # The descriptive term that is used to identify whether or not the product claims to provide waterproofing to the applied surface.
    isWearableItemDisposable: URIRef  # Identifies whether or not the product is intended to be disposed of after single use or a limited period of use.
    itemOffered: URIRef  # The product included in the offer.
    juiceContentPercent: (
        URIRef  # The fruit juice content of the product expressed as a percentage.
    )
    jws: URIRef  # A link to a JSON Web Signature
    latitude: URIRef  # Angular distance North or South from the earth's equator measured through 90 degrees.
    leasedFrom: (
        URIRef  # Links to the organisation (lessor) from which this place is leased.
    )
    leasedTo: URIRef  # Links to the organisation(s) (lessee(s)) to which this place is leased. Property SHOULD be applied to a specific sub-location, rather than a main location, wherever possible.
    leaveReview: URIRef  # A link through which a review can be added.
    lesseeOf: URIRef  # Links to the place(s) for which this organisation is the lessee (i.e., this organisation leases those places from another organisation, the lessor).
    lessorFor: URIRef  # Links to the place(s) for which this organisation is the lessor (i.e., this organisation leases those places to others).
    line: URIRef  # A line is a point-to-point path consisting of two or more point objects separated by a space. A single line segment (i.e., straight line) is expressed as two points.  A multi-line path (i.e., open polygon) is expressed as a series of three or more points. For a closed shape, gs1:polygon SHALL be used.
    linkType: URIRef  # Provides a URL for related information or services. This is not expected to be used directly but provides a super property for all other link types in the GS1 ecosystem.
    location: URIRef  # The place(s) associated with an organization.
    locationGLN: URIRef  # 13-digit GLN that is being used to identify a physical or digital location. If gs1:glnType is present, gs1:locationGLN SHALL only be used when gs1:GLN_TypeCode includes FIXED_PHYSICAL_LOCATION, MOBILE_PHYSICAL_LOCATION, or DIGITAL_LOCATION
    locationHistory: (
        URIRef  # Provides details on if and when a location is active or inactive.
    )
    locationID: URIRef  # Identifier value associated to a location. This value SHALL follow rules set forth by the administrating organisation designated in gs1:LocationID_Type.
    locationID_Qualifier: URIRef  # Secondary qualifier to supplement gs1:LocationID_Type meaning. May be used with proprietary ID code values to define identifier administrator.
    locationID_Type: URIRef  # Organisation that administers the gs1:locationID or the name of the ID itself.  Value from gs1:LocationID_Type code list.
    locationID_URI: URIRef  # A URI that links to information about the gs1:locationID.
    locationInfo: URIRef  # A link to a map, directions, or other location-related information.  For B2B location  information, see gs1:logisticsInfo.  For details specific to hours of operation, see gs1:openingHoursInfo
    locationRole: URIRef  # A location classification based on the purpose, type of site and/or what occurs there. Repeatable value from gs1:LocationRoleType code list.
    locationStatus: URIRef  # Designation of active/inactive status of a location.
    logisticsInfo: (
        URIRef  # A link to B2B logistics information related to a physical location.
    )
    longitude: URIRef  # The arc or portion of the earth's equator intersected between the meridian of a given place and the prime meridian and expressed in degrees
    loyaltyProgram: URIRef  # A link to information about a loyalty program, including a member's current status and/or a registration option for new members
    magnesiumPerNutrientBasis: (
        URIRef  # Magnesium per specified nutrient basis quantity.
    )
    makesOffer: URIRef  # An offer made by an organization.
    managedBy: URIRef  # Links to the organisation that manages this place or organisation, as designated by the owner or another organisation.
    managedFor: URIRef  # Links to the organisation(s) for whom this place is managed. Property SHOULD be applied to a specific sub-location, rather than a main location, wherever possible.
    manages: URIRef  # Links to the place(s) or organisation(s) that this organisation manages, on behalf of the owner or another organisation.
    manganesePerNutrientBasis: (
        URIRef  # Manganese per specified nutrient basis quantity.
    )
    manufacturer: URIRef  # The organization that produces the item.
    manufacturerPreparationCode: URIRef  # Code indicating the preparation methods that a manufacturer has used in the manufacturing of a product for example DEEP_FRY.
    manufacturersWarranty: URIRef  # The warranty associated with the product.
    manufacturingPlant: URIRef  # A physical location consisting of one or more buildings with facilities for manufacturing.
    massPerUnitArea: URIRef  # The mass per unit area of the item. This can be given using a number of different AI ranges that depend on the units in which the mass and area are measured.
    masterData: URIRef  # A link to a source of structured master data for the entity. This is typically for B2B applications.
    maturationMethod: URIRef  # The method of maturity for the item for example tree ripened or jet fresh.
    maxPrice: URIRef  # Provides a maximum price value as a floating-point numeric value that is qualified by the corresponding currency. See also gs1:priceCurrency
    maximumDiscountAmount: URIRef  # Links to a gs1:PriceSpecification that indicates in terms of an amount and specified currency, the maximum discount on the sales price associated with a particular gs1:Discount. This property can be used to express 'up to $10 off'.
    maximumDiscountPercentage: URIRef  # A floating-point value indicating a maximum percentage discount on the sales price associated with a particular gs1:Discount.  This property can be used to express 'up to 15% discount'.
    maximumOptimumConsumptionTemperature: URIRef  # The upper limit drinking temperature of the optimum range of the drinking temperature. The optimum range of the drinking temperature is a recommendation and is based on the experience of the individual producer. Allows for the representation of the same value in different units of measure but not multiple values.
    maximumQualifyingItems: URIRef  # Specifies the maximum number of items that qualify for a particular gs1:Discount. This property can be used to express 'maximum N items per customer'.
    maximumQualifyingSpend: URIRef  # Links to a gs1:PriceSpecification that indicates in terms of an amount and specified currency, the maximum spend that qualifies for a particular gs1:Discount. This property can be used to express 'for purchases of up to $100'.
    meatPoultryType: (
        URIRef  # The fish, meat, or poultry type for this food and beverage item.
    )
    menuInfo: URIRef  # A link to menu details. This may include food menus, services, or other offerings provided by an organisation or at a location.  For details specific to allergens only, see gs1:allergenInfo .  For details specific to nutrition information only, see gs1:nutritionalInfo .  For details specific to ingredients only, see gs1:ingredientsInfo .
    minPrice: URIRef  # Provides a minimum price value as a floating-point numeric value that is qualified by the corresponding currency. See also gs1:priceCurrency
    minimumDiscountAmount: URIRef  # Links to a gs1:PriceSpecification that indicates in terms of an amount and specified currency, the minimum discount on the sales price associated with a particular gs1:Discount. This property can be used to express 'at least $10 off'.
    minimumDiscountPercentage: URIRef  # A floating-point value indicating a minimum percentage discount on the sales price associated with a particular gs1:Discount.  This property can be used to express 'at least 15% discount'.
    minimumFishContent: URIRef  # The minimum amount of fish contained in a food and beverage product expressed as a measurement.
    minimumMeatPoultryContent: URIRef  # The minimum amount of fish, meat or poultry contained in a food and beverage product expressed as a measurement.
    minimumOptimumConsumptionTemperature: URIRef  # The lower limit drinking temperature of the optimum range of the drinking temperature. The optimum range of the drinking temperature is a recommendation and is based on the experience of the individual producer. Allows for the representation of the same value in different units of measure but not multiple values.
    minimumQualifyingItems: URIRef  # Specifies the minimum number of items that must be purchased to qualify for a particular gs1:Discount. This property can be used to express 'if you buy at least N items'.
    minimumQualifyingSpend: URIRef  # Links to a gs1:PriceSpecification that indicates in terms of an amount and specified currency, the minimum spend required to qualify for a particular gs1:Discount. This property can be used to express 'if you spend at least $100'.
    molybdenumPerNutrientBasis: (
        URIRef  # Molybdenum per specified nutrient basis quantity.
    )
    monounsaturatedFatPerNutrientBasis: (
        URIRef  # Monounsaturated fat per specified nutrient basis quantity.
    )
    netArea: URIRef  # The net area of the item. This can be given using a number of different AI ranges that depend on the units in which the area is measured.
    netContent: URIRef  # The quantity of the product contained by a package, usually as claimed on the label. Indicates the net content of the total product. For fixed value products use the value claimed on the package, to avoid variable fill rate issue that arises with some product which are sold by volume or weight, and whose actual content may vary slightly from batch to batch.
    netWeight: URIRef  # Used to identify the net weight of the product. Net Weight excludes all packaging material, including the packaging material of all lower-level GTINs. Example:11.5 kgm.
    niacinPerNutrientBasis: URIRef  # Niacin per specified nutrient basis quantity.
    numberOfServingsPerPackage: (
        URIRef  # The total number of servings contained in the package.
    )
    numberOfServingsPerPackageMeasurementPrecision: URIRef  # Code indicating whether the number of servings per package is exact or approximate.
    numberOfServingsRangeDescription: URIRef  # A free text field specifying a range for the number of servings contained in the package.
    nutrientBasisQuantity: URIRef  # Quantity on which the nutrient information has been based; for example, per 100 grams. When specified, nutrientBasisQuantity establishes the basis for all contained nutrient records.
    nutrientBasisQuantityType: URIRef  # The type of quantity specified in the nutrientBasisQuantity for example measurement, serving size, or container. This is used in conjunction with the nutrientBasisQuantity.
    nutrientMeasurementPrecision: URIRef  # The Code indicating whether the specified nutrient content is exact or approximate.
    nutritionalClaim: URIRef  # Code indicating a nutritional claim applicable to the product, for example FAT_FREE.
    nutritionalClaimStatement: (
        URIRef  # Free text field for any additional nutritional claims.
    )
    nutritionalInfo: URIRef  # A link to nutritional facts.
    occupiedBy: URIRef  # Links to the organisation(s) that occupy this place. Property SHOULD be applied to a specific sub-location, rather than a main location, wherever possible.
    occupies: URIRef  # Links to the place(s) that this organisation occupies.
    offerDescription: URIRef  # A description of the offer including goods or services offered for sale or use.
    offerDiscount: URIRef  # A discount associated with an offer.
    offerRedemptionType: URIRef  # A code indicating the type of redemptions that apply to the offer, for example single use.
    offerRedemptionURL: URIRef  # The URL where the offer seeker will need to go in order to redeem the offer for an online redemption.
    offerRestrictionDescription: URIRef  # A description of what the offer is restricted to, relative to all other offerings by the issuer, for example payment restrictions, subscription required, new customers only.
    openingHoursInfo: URIRef  # A link to details on hours of operation.
    organicClaim: URIRef  # Relates to an organic claim about the product
    organicClaimAgency: URIRef  # A governing body that creates and maintains standards related to organic products.
    organicPercentClaim: URIRef  # The percent of actual organic materials per weight of the product. This is usually claimed on the product.
    organizationHistory: URIRef  # Provides details on if and when an organisation/party is active or inactive.
    organizationID: URIRef  # Identifier value associated to an organisation/party. This value SHALL follow rules set forth by the administrating organisation designated in gs1:OrganizationID_Type.
    organizationID_Qualifier: URIRef  # Secondary qualifier to supplement gs1:organizationID_Type meaning. May be used with proprietary ID code values to define identifier administrator.
    organizationID_Type: URIRef  # Organisation that administers the gs1:organizationID or the name of the ID itself.  Value from gs1:OrganizationID_Type code list.
    organizationID_URI: (
        URIRef  # A URI that links to information about the gs1:organizationID.
    )
    organizationName: URIRef  # The name of the organization expressed in text.
    organizationRole: URIRef  # The role and/or purpose of a party (i.e. legal entity or function).  Multiple values from gs1:OrganizationRoleType code list may be associated to a single organisation/party.
    organizationStatus: (
        URIRef  # Designation of active/inactive status of an organisation/party.
    )
    originalCodeValue: URIRef  # Links to the alphanumeric code value defined elsewhere in GS1 or the GS1 Global Data Dictionary
    outOfPackageDepth: URIRef  # The depth of the product out of its packaging, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    outOfPackageDiameter: URIRef  # The measurement of the diameter of the product out of its package at its largest point. For example, 165 MMT.
    outOfPackageHeight: URIRef  # The height of the product out of the package, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    outOfPackageWidth: URIRef  # The width of the product out of the package, as measured according to the GS1 Package Measurement Rules. See https://www.gs1.org/package-measurement-rules-implementation-guide for more details.
    ownedBy: URIRef  # Links to the organisation(s) that own this place, in full or in part. This includes joint ventures. For leased locations, see gs1:lessorFor and gs1:isLeasedFrom.
    owns: (
        URIRef  # Links to the place(s) or organisation(s) that this organisation owns.
    )
    packaging: URIRef  # Details on the packaging for a product including type, weight and materials.
    packagingDate: URIRef  # The packaging date is the date when the goods were packed as determined by the packager. The date may refer to the trade item itself or to items contained.
    packagingFeature: URIRef  # Code indicating a feature that facilitates the usage of the product by the consumer, for example a handle. Packaging features do not affect the core composition of the packaging type nor modify its usage.
    packagingFunction: URIRef  # Code indicating specific functionality for packaging resulting from specific processes or features present in the packaging type,for example, ANTI_TAMPERING.
    packagingMarkedDietAllergenType: (
        URIRef  # Indication of which dietary or allergen marks are on the package.
    )
    packagingMarkedFreeFrom: URIRef  # Indication of the food ingredients that the package is marked free from.
    packagingMarkedLabelAccreditation: URIRef  # A marking that the product received recognition, endorsement, certification by following guidelines by the label issuing agency. This does not represent claims for regulatory purposes on products such as free from markings.
    packagingMaterial: (
        URIRef  # links to details about packaging material type, quantity and thickness
    )
    packagingMaterialCompositionQuantity: URIRef  # The quantity of the packaging material of the product. Can be weight, volume or surface, can vary by country.
    packagingMaterialThickness: URIRef  # The thickness of a packaging material.
    packagingMaterialType: URIRef  # The materials used for the packaging of the product for example glass or plastic.
    packagingRecyclingProcessType: URIRef  # The process the packaging could undertake for recyclable & sustainability programs. Examples COMPOSTABLE, ENERGY_RECOVERABLE, REUSABLE.
    packagingRecyclingScheme: URIRef  # A code indicating the recycling scheme the packaging of this product will fall within when recycled. Applies to recyclable packaging with or without deposit.
    packagingShape: URIRef  # A code depicting the shape of a package for example CONE.
    packagingType: URIRef  # The dominant means used to transport, store, handle or display the product as defined by the data source. This packaging is not used to describe any manufacturing process.Recommend to use UNECE Rec 21 codes.
    pantothenicAcidPerNutrientBasis: (
        URIRef  # Pantothenic Acid per specified nutrient basis quantity.
    )
    parentOrganization: URIRef  # Designates the legal entity or function directly above the organisation/party being identified in a hierarchy. This is not defaulted to the highest-level entity in the hierarchy. Only one parent organisation SHALL be associated to a single GLN. To specify other affiliated organisations, see gs1:affiliatedTo, gs1:managedBy, gs1:franchiseeOf, gs1:ownedBy. To specify an organisation/party lower in the hierarchy, see gs1:subOrganization.
    partyGLN: URIRef  # 13-digit GLN that is being used to identify a legal entity or function. If gs1:glnType is present, gs1:partyGLN SHALL only be used when gs1:GLN_TypeCode includes LEGAL_ENTITY and/or FUNCTION
    paymentLink: URIRef  # A link to a place where payments details are provided and/or payments can be made by the user.
    paymentTerms: (
        URIRef  # The type of payment term expressed as a code, for example Discount.
    )
    percentageOfAlcoholByVolume: (
        URIRef  # The percentage of alcohol contained in product.
    )
    phosphorusPerNutrientBasis: (
        URIRef  # Phosphorus per specified nutrient basis quantity.
    )
    physicalLocationName: URIRef  # The name of a physical place. To specify the name of a digital location, see gs1:digitalLocationName.
    pip: URIRef  # A link to information specifically about the identified item, typically operated by the brand owner or a retailer of the product and aimed at consumers. It may include links to further information, product description, specifications etc.
    polygon: URIRef  # A polygon is the area enclosed by a point-to-point path for which the starting and ending points are the same. A polygon is expressed as a series of four or more space delimited points where the first and final points are identical.
    polyolsPerNutrientBasis: URIRef  # Polyols per specified nutrient basis quantity.
    polyunsaturatedFatPerNutrientBasis: (
        URIRef  # Polyunsaturated fat per specified nutrient basis quantity.
    )
    postOfficeBoxNumber: URIRef  # The number that identifies a PO box. A PO box is a box in a post office or other postal service location assigned to an organization where postal items may be kept.
    postalCode: URIRef  # Text specifying the postal code for an address.
    postalName: URIRef  # The name of the recipient expressed in text. Note that this may be different than gs1:OrganizationName.
    potassiumPerNutrientBasis: (
        URIRef  # Potassium per specified nutrient basis quantity.
    )
    preparationCode: URIRef  # Code specifying the preparation state of the product for which the nutrient information is valid. PREPARED, UNPREPARED.
    preparationConsumptionPrecautions: URIRef  # Specifies additional precautions to be taken before preparation or consumption of the product.
    preparationInformation: URIRef  # Links to information about how to prepare a specific Food/Beverage/Tobacco product.
    preparationInstructions: URIRef  # Free text providing instructions on how to prepare the product before serving.
    preservationTechnique: URIRef  # Code indicating the preservation technique used to preserve the product from deterioration, for example, BRINING.
    price: URIRef  # Provides a price value as a floating-point numeric value that is qualified by the corresponding currency. See also gs1:priceCurrency. The price value indicates the unit price unless the property gs1:eligibleQuantity is specified and indicates multiple units
    priceCurrency: (
        URIRef  # A string value indicating a currency from ISO 4217 for example USD .
    )
    priceSpecification: URIRef  # The price related to an offer. If the offer is a multi-buy offer for a quantity of product greater than one unit, this should be indicated using the property gs1:eligibleQuantity
    primaryAlternateProduct: URIRef  # A product that is similar to the current product but is not exact match. Same form fit function, e.g. same product different colour, different package size, better quality.
    primaryLocationOf: URIRef  # Links to the organisation(s) that designate this place as its/their primary location. Property SHOULD be applied to a specific sub-location, rather than a main location, wherever possible.
    productDescription: URIRef  # An understandable and useable description of a product using brand and other descriptors. This attribute is filled with as little abbreviation as possible, while keeping to a reasonable length.  This should be a meaningful description of the product with full spelling to facilitate message processing. Retailers can use this description as the base to fully understand the brand, flavour, scent etc. of the specific product, in order to accurately create a product description as needed for their internal systems. Examples: XYZ Brand Base Invisible Solid Deodorant AP Stick Spring Breeze.
    productFeatureBenefit: URIRef  # Element for consumer facing marketing content to describe the key features or benefits of the style suitable for display purposes.
    productFormDescription: URIRef  # The physical form or shape of the product. Used, for example, in pharmaceutical industry to indicate the formulation of the product. Defines the form the product takes and is distinct from the form of the packaging.
    productID: URIRef  # Additional means to the Global Trade Item Number to identify a product.
    productMarketingMessage: URIRef  # Marketing message associated with the product. Consumer-friendly marketing detailed description of the product.
    productName: URIRef  # Consumer friendly short description of the product suitable for compact presentation.
    productRange: URIRef  # A name, used by a Brand Owner, that span multiple consumer categories or uses. E.g. (Waist Watchers).
    productSustainabilityInfo: URIRef  # This term has been deprecated. Please use gs1:sustainabilityInfo instead.
    productYield: URIRef  # Product quantity after preparation. This can differ based on productYieldType
    productYieldType: URIRef  # Code indicating the type of yield measurement specified in productYield. Examples: AFTER_DILUTION, DRAINED_WEIGHT.
    productYieldVariationPercentage: URIRef  # Indication of range in percent of the given cooking / roasting loss. Percentage that the actual weight of the product differs upward or downward from the average or estimated product yield.
    productionDate: URIRef  # The production date is the production or assembly date determined by the manufacturer. The date may refer to the trade item itself or to items contained.
    productionDateTime: URIRef  # The date and time of production (or assembly). The date and time of production is determined by the manufacturer. The date and time may refer to the trade item itself or to the items contained.
    productionVariantDescription: URIRef  # Free text assigned by the manufacturer to describe the production variant. Examples are: package series X, package series Y.
    productionVariantEffectiveDateTime: URIRef  # The start date of a production variant. The variant applies to products having a date mark (a best before date or expiration date) on the package that comes on or after the effective date.
    promotion: URIRef  # A link to a promotion.
    proteinPerNutrientBasis: URIRef  # Protein per specified nutrient basis quantity.
    provenanceStatement: URIRef  # Free text description of the region or place the product originates from. This is to be specifically used to specify areas such as cities, mountain ranges, regions. Examples: Made in the Thuringen Mountains, Made in Paris, From the Napa Valley.
    purchaseSuppliesOrAccessories: URIRef  # A link to information about where supplies or accessories for the item can be purchased or ordered.
    qualifyingBrandName: URIRef  # If specified, the discount is only available when purchasing a product from one of the brand names specified via this property.
    qualifyingGPCs: URIRef  # If specified, the discount is only available when purchasing a product whose Global Product Classification (GPC) brick value appears in the list specified via this property.
    qualifyingProductCategoryDescription: URIRef  # If specified, the discount is only available when purchasing a product from categories specified in this free-form text field.
    qualifyingProductClassificationCode: URIRef  # If specified, the discount is only available when purchasing a product whose product classification (other than GPC) appears in the list specified via this property. This property specifies a product classification other than GPC.
    qualifyingProductGTINs: URIRef  # If specified, the discount is only available when purchasing a product whose GTIN appears in the list specified via this property.
    qualifyingSubBrandName: URIRef  # If specified, the discount is only available when purchasing a product from one of the sub-brand names (specified product ranges for a given brand) specified via this property.
    quickStartGuide: URIRef  # A link to a description of the key features needed to be understood to begin using the item or interacting with something new.
    recallStatus: URIRef  # A link to information about whether the product has been recalled or not, typically an API.
    recipeInfo: URIRef  # A link to a recipe website.
    referencedFile: URIRef  # Link to a file or website containing additional information on product.
    referencedFileEffectiveEndDateTime: URIRef  # The date upon which the target of this external link ceases to be effective for use.
    referencedFileEffectiveStartDateTime: URIRef  # The date upon which the target of this external link begins to be effective for use.
    referencedFileSize: (
        URIRef  # The size of the file as it is stored in an uncompressed format.
    )
    referencedFileType: URIRef  # A code indicating the purpose or role of file (not a MIME type) that is being referenced, for example PRODUCT_LABEL_IMAGE. This code is used when the purpose of a file is not specified in the property.
    referencedFileURL: URIRef  # Simple text string that refers to a resource on the internet, URLs may refer to documents, resources, people, etc.
    registerProduct: URIRef  # A link to an entry point for registering ownership of a product including for warranty purposes.
    registryEntry: URIRef  # A link to an entry in a register, such as a business register or register of locations. Such registers may act as alternative identifiers, such as official company numbers, LEIs, other location identifiers etc.
    regulatedProductName: URIRef  # The prescribed, regulated or generic product name or denomination that describes the true nature of the product. For example for a food product in order to distinguish it from other foods according to country specific regulations.
    reheatingClaim: URIRef  # Indicates, with reference to the product branding, labelling or packaging whether a food product which is ready to eat can be reheated if required prior to consumption.
    relatedImage: URIRef  # A link to any image that depicts or relates to the identified entity (e.g., trade item, assets, business process, patient record, location, organisation, etc.)
    relatedOrganization: URIRef  # The organisation(s) associated with a place.
    relatedVideo: URIRef  # A link to any video, or document that has an embedded video, that describes or relates to the identified item, organisation, or location in some way.
    replacedByOrganization: URIRef  # Links to the successor organisation that is used in place of a previous organisation
    replacedByPlace: URIRef  # Links to the successor location that is used in place of a previous location
    replacedByProduct: URIRef  # The product which permanently replaces the current product. This product is sent in the record for the original item that is being replaced.
    replacedOrganization: (
        URIRef  # Links to the previous organisation that this organisation replaces
    )
    replacedPlace: URIRef  # Links to the previous location that this location replaces
    replacedProduct: URIRef  # Indicates the product identification of an item that is being permanently replaced by this product.
    responsibility: URIRef  # Text further specifying the area of responsibility of the trade contact.
    responsibleForLocation: (
        URIRef  # Links to the place(s) for which this organisation is responsible.
    )
    responsibleOrganization: (
        URIRef  # Links to the organisation that is directly responsible for this place.
    )
    restricted: URIRef
    returnablePackageDepositAmount: (
        URIRef  # The monetary amount for the individual returnable package.
    )
    returnablePackageDepositRegion: URIRef  # The geographic region associated with the returnable package deposit amount.
    review: URIRef  # A link to reviews.
    riboflavinPerNutrientBasis: (
        URIRef  # Riboflavin per specified nutrient basis quantity.
    )
    safetyInfo: URIRef  # A link to safety information.
    saltPerNutrientBasis: URIRef  # Salt per specified nutrient basis quantity.
    saturatedFatPerNutrientBasis: (
        URIRef  # Saturated fat per specified nutrient basis quantity.
    )
    scheduleTime: URIRef  # A link to a site that offers information on scheduling, appointments, or reservations. This may or may not allow the user to book the reservation.
    seasonCalendarYear: (
        URIRef  # The calendar year in which the product is seasonally available.
    )
    seasonName: (
        URIRef  # Element defines the season applicable to the item for example Winter.
    )
    seasonParameter: URIRef  # Code indicating the season in which the product is available, e.g. SPRING, WINTER
    seeker: URIRef  # The organization seeking an offer.
    selectedProductsOnly: URIRef  # If specified and set to true, the discount only applies to specific products selected by the retailer or offer promoter - not to all items in that product category.  This property should be asserted and set to true for offers that say 'on selected products'.
    seleniumPerNutrientBasis: URIRef  # Selenium per specified nutrient basis quantity.
    sellByDate: URIRef  # The date specified by the manufacturer as the last date the retailer is to offer the product for sale to the consumer. The product should not be merchandised after this date.
    seller: URIRef  # The organization seeking to sell a product or service.
    serviceInfo: URIRef  # A link to service or maintenance instructions.
    servingSize: URIRef  # Measurement value specifying the serving size in which the information per nutrient has been stated. Example: Per 100 GRM.
    servingSizeDescription: URIRef  # A free text field specifying the serving size for which the nutrient information has been stated for example: per 1/3 cup (42 g).
    servingSuggestion: URIRef  # Free text field for serving suggestion.
    sharpnessOfCheese: URIRef  # The descriptive term that is used by the product manufacturer to identify the sharpness of the taste of the product for example EXTRA_SHARP. Usually the longer the aging of the product, the sharper the taste.
    size: URIRef  # Links a wearable product to one or more groupings of gs1:SizeDetails representing size systems, size groups, size type and size dimensions.
    sizeCode: URIRef  # Links a product to one or more groupings of gs1:SizeCodeDetails representing the size value from a specified code list.
    sizeCodeListCode: URIRef  # Code specifying a size code list. Allowed code values are specified in GS1 Code List SizeCodeListCode .
    sizeCodeValue: URIRef  # A code indicating the size of an object according to a specific code list. The applied code list is specified as additional information together with the size code.
    sizeDimension: URIRef  # The numerical size measurement relating to the size type.
    sizeGroup: URIRef  # Code indicating the type of size that is necessary to uniquely specify the size of the item, for example, BOYS.
    sizeSystem: URIRef  # The system that is being used to define the size for example EUROPE. Size system is used in conjunction with size group to define the size dimension.
    sizeType: URIRef  # The type of size dimension being specified for example SLEEVE.
    smartLabel: URIRef  # A link to the product's SmartLabel page.
    smpc: URIRef  # A link to Summary Product Characteristics. To be used specifically when linking to information for healthcare professionals.
    socialMedia: URIRef  # A link to a social media channel. The title will typically be replaced by the name of the channel.
    sodiumPerNutrientBasis: URIRef  # Sodium per specified nutrient basis quantity.
    sourceAnimal: URIRef  # Code indicating the source of raw material used to produce the food product, for example a GOAT for milk.
    sportingActivityType: URIRef  # Code indicating the type of sporting activity for which the product is intended to be worn, for example FOOTBALL.
    starchPerNutrientBasis: URIRef  # Starch per specified nutrient basis quantity.
    statisticInfo: URIRef  # A link to information about statistics regarding an organisation, location, or other entity.
    statusTimestamp: URIRef  # Date and time (including optional timezone) associated to status designations. Timestamps may be future dated to provide advance notice of status changes. For further information about the required lexical representation of date, time, and timezone please see https://www.w3.org/TR/xmlschema-2/#dateTime
    streetAddress: URIRef  # The street address expressed as free form text. The street address is printed on paper as the first lines below the name. For example, the name of the street and the number in the street or the name of a building. A total of four street address lines are available. gs1:streetAddress SHOULD be used before populating lines two through four. For a PO Box gs1:postOfficeBoxNumber SHOULD be used instead.
    streetAddressLine2: URIRef  # The second line of the street address, expressed as free form text. The street address is printed on paper as the first lines below the name. For example, the name of the street and the number in the street or the name of a building. A total of four street address lines are available. gs1:streetAddress SHOULD be used before populating lines two through four. These SHALL NOT be used as alternatives to the dedicated address properties gs1:addressSuburb, gs1:addressLocality and gs1:addressRegion.
    streetAddressLine3: URIRef  # The third line of the street address, expressed as free form text. The street address is printed on paper as the first lines below the name. For example, the name of the street and the number in the street or the name of a building. A total of four street address lines are available. gs1:streetAddress and gs1:streetaddressLine2 SHOULD be used before populating lines three and four. These SHALL NOT be used as alternatives to the dedicated address properties gs1:addressSuburb, gs1:addressLocality and gs1:addressRegion.
    streetAddressLine4: URIRef  # The fourth line of the street address, expressed as free form text. The street address is printed on paper as the first lines below the name. For example, the name of the street and the number in the street or the name of a building. gs1:streetAddress, gs1:streetaddressLine2 and gs1:streetaddressLine3 SHOULD be used before populating line four. These SHALL NOT be used as alternatives to the dedicated address properties gs1:addressSuburb, gs1:addressLocality and gs1:addressRegion.
    styleDescription: URIRef  # An attribute that classifies products that share many of the same characteristics (attribute values) that does NOT vary by GTIN, and are presented by the supplier as a single merchandise selection for the buyer.
    subBrandName: URIRef  # Second level of brand. Can be a trademark. It is the primary differentiating factor that a brand owner wants to communicate to the consumer or buyer. E.g. Yummy-Cola Classic. In this example Yummy-Cola is the brand and Classic is the sub-brand.
    subOrganization: URIRef  # Designates a legal entity or function directly below the organisation/party being identified in a hierarchy. There may be multiple sub-organisations associated to a single GLN. To specify other affiliated organisations, see gs1:manages, gs1:franchisorOf, gs1:owns. To specify a parent organisation, see gs1:parentOrganization.
    subscribe: URIRef  # A link to a subscription form
    sugarsPerNutrientBasis: URIRef  # Sugars per specified nutrient basis quantity.
    supplierSpecifiedMinimumConsumerStorageDays: URIRef  # Represents the number of days between a product's sell by date and its use by date.
    support: URIRef  # A link to a source of support such as a helpdesk, chat support, email etc.
    sustainabilityInfo: URIRef  # A link to information relating to sustainability and recycling requirements or processes.
    targetConsumerAge: URIRef  # Identifies the target consumer age range for which a product has been designed.
    targetConsumerGender: URIRef  # Identifies the target consumer gender for which a product has been designed for example MALE
    targetMarket: URIRef  # Relates to a set of target market details (product release date and associated countries)
    targetMarketCountries: URIRef  # List of countries representing the target market for a particular release date indicated by gs1:consumerFirstAvailabilityDateTime
    telephone: URIRef  # A telephone number for example +44 217 992 9999.
    textileMaterial: URIRef  # One or more links to information about the materials used in a wearable product.
    textileMaterialContent: URIRef  # A description of the material composition used in conjunction with the material percentage.
    textileMaterialDescription: URIRef  # This provides a name or brief description of one material contained within the product, for example Rayon.
    textileMaterialPercentage: URIRef  # Corresponding net weight percentage of the product material specified via gs1:textileMaterialDescription, e.g. 70.
    textileMaterialThreadCount: URIRef  # The quality of material (fabric) of a product based on the total number of vertical and horizontal threads in one square inch.
    textileMaterialWeight: URIRef  # The measured weight of the material expressed in ounces per square yard or grams per square meter.
    thiaminPerNutrientBasis: URIRef  # Thiamin per specified nutrient basis quantity.
    traceability: URIRef  # A link to traceability information (includes track and trace).  Traceability information may be provided for consumption by humans or computers. If the target is an EPCIS repository, use gs1:epcis instead.
    transFatPerNutrientBasis: URIRef  # Trans Fat per specified nutrient basis quantity.
    tutorial: URIRef  # A link to a tutorial or set of tutorials, such as online classes, how-to videos etc.
    unitCode: URIRef  # A string value indicating a Measurement Unit from UN/ECE Recommendation 20, Units of Measure used in International Trade e.g. GRM = gram - see http://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_rev3_Annex3e.pdf
    upperMaterialType: URIRef  # The material(s) used for the upper part of the footwear product. The upper is the part of a shoe, boot, slipper or other item of footwear that is above the sole.
    userAgreement: URIRef  # A link to an agreement or waiver.
    usesManagedLocation: (
        URIRef  # Links to the place(s) that this organisation uses as a managed space.
    )
    validFrom: URIRef  # The effective start date of the price .
    validThrough: URIRef  # The effective end date of the price .
    value: URIRef  # A floating-point numeric value that is qualified by the corresponding measurement unit code - see gs1:unitCode
    variantDescription: URIRef  # Free text field used to identify the variant of the product. Variants are the distinguishing characteristics that differentiate products with the same brand and size including such things as the particular flavour, fragrance, taste.
    verificationService: URIRef  # A link to a GS1 Lightweight Messaging Service for verifying the status of a product, organisation, or location and its identifier.
    vintner: URIRef  # The person hired by a winery or wine company who is responsible for many of the processes in the preparation, taste and quality of the wine produced. The science of wine making is referred to as oenology. The vintner is the oenologist.
    vitaminAPerNutrientBasis: URIRef  # Vitamin A per specified nutrient basis quantity.
    vitaminB12PerNutrientBasis: (
        URIRef  # Vitamin B12 per specified nutrient basis quantity.
    )
    vitaminB6PerNutrientBasis: (
        URIRef  # Vitamin B6 per specified nutrient basis quantity.
    )
    vitaminCPerNutrientBasis: URIRef  # Vitamin C per specified nutrient basis quantity.
    vitaminDPerNutrientBasis: URIRef  # Vitamin D per specified nutrient basis quantity.
    vitaminEPerNutrientBasis: URIRef  # Vitamin E per specified nutrient basis quantity.
    vitaminKPerNutrientBasis: URIRef  # Vitamin K per specified nutrient basis quantity.
    warningCopyDescription: URIRef  # Warning information is additional information that outlines special requirements, warning and caution information printed on the package.
    warranty: URIRef  # The warranty associated with the product, as provided by the manufacturer.
    warrantyScopeDescription: URIRef  # The description of warranty available for the product. Allows for the representation of the same value in different languages but not for multiple values.
    whatsInTheBox: URIRef  # A link to a description of all the individual items in a packaged item.
    yield_: URIRef  # Product quantity after preparation.
    zincPerNutrientBasis: URIRef  # Zinc per specified nutrient basis quantity.
