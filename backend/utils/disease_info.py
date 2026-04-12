"""
Disease Information Database
=============================
Contains detailed information about each skin disease including:
- Description
- Symptoms
- Treatment recommendations
- Prevention tips
- Severity level

This information is displayed to users after prediction.
"""

DISEASE_INFO = {
    "Melanocytic nevi": {
        "description": "Melanocytic nevi, commonly known as moles, are benign growths of melanocytes (pigment-producing cells). They are very common and usually harmless. Most adults have between 10-40 moles.",
        "symptoms": [
            "Uniform brown, tan, or black color",
            "Flat or slightly raised",
            "Symmetrical shape",
            "Smooth borders",
            "Usually less than 6mm in diameter"
        ],
        "treatment": "Most melanocytic nevi do not require treatment. Monitor for any changes in size, shape, color, or texture. If concerned about cosmetic appearance or if the mole is frequently irritated, surgical removal may be considered.",
        "precautions": [
            "Perform regular skin self-examinations",
            "Protect moles from excessive sun exposure",
            "Use sunscreen with SPF 30 or higher",
            "See a dermatologist if you notice changes (ABCDE rule: Asymmetry, Border, Color, Diameter, Evolving)",
            "Avoid tanning beds"
        ],
        "severity": "Low",
        "consultation": "Routine check-ups recommended. Consult if changes are observed."
    },
    
    "Melanoma": {
        "description": "Melanoma is a serious form of skin cancer that develops in melanocytes. It can spread to other parts of the body if not caught early. Early detection is crucial for successful treatment.",
        "symptoms": [
            "Asymmetrical shape",
            "Irregular, scalloped, or poorly defined borders",
            "Multiple colors or uneven color distribution",
            "Larger than 6mm in diameter",
            "Evolving in size, shape, or color",
            "Itching, bleeding, or crusting"
        ],
        "treatment": "Immediate medical attention required. Treatment options include surgical excision, immunotherapy, targeted therapy, chemotherapy, or radiation therapy depending on the stage. Early-stage melanoma has a high cure rate with surgical removal.",
        "precautions": [
            "Seek immediate dermatological consultation",
            "Do not delay treatment",
            "Protect skin from UV radiation",
            "Regular follow-up appointments",
            "Full-body skin examinations every 3-6 months",
            "Inform family members (genetic component)"
        ],
        "severity": "High",
        "consultation": "URGENT: Consult a dermatologist or oncologist immediately."
    },
    
    "Benign keratosis-like lesions": {
        "description": "Benign keratosis-like lesions include seborrheic keratoses and solar lentigines (age spots or liver spots). These are common, non-cancerous skin growths that typically appear in middle-aged and older adults.",
        "symptoms": [
            "Waxy, scaly, slightly raised growths",
            "Tan, brown, or black in color",
            "Round or oval shape",
            "Stuck-on appearance",
            "May itch or become irritated"
        ],
        "treatment": "Treatment is usually not necessary as these lesions are benign. For cosmetic reasons or if irritated, options include cryotherapy (freezing), curettage (scraping), electrocautery, or laser therapy.",
        "precautions": [
            "Avoid scratching or picking at lesions",
            "Use sunscreen daily",
            "Wear protective clothing outdoors",
            "Monitor for any changes",
            "Consult dermatologist if lesions become painful or bleed"
        ],
        "severity": "Low",
        "consultation": "Non-urgent. Consult for cosmetic removal or if lesions change."
    },
    
    "Basal cell carcinoma": {
        "description": "Basal cell carcinoma (BCC) is the most common type of skin cancer. It develops in the basal cells of the epidermis. While it rarely spreads to other parts of the body, it can cause significant local damage if untreated.",
        "symptoms": [
            "Pearly or waxy bump",
            "Flat, flesh-colored or brown scar-like lesion",
            "Bleeding or scabbing sore that heals and returns",
            "Pink growth with raised edges and crusted center",
            "Visible blood vessels in the lesion"
        ],
        "treatment": "Treatment is highly effective and includes surgical excision, Mohs surgery, cryosurgery, curettage and electrodesiccation, or topical medications. Early treatment prevents tissue damage.",
        "precautions": [
            "See a dermatologist promptly for treatment",
            "Protect skin from sun exposure",
            "Use broad-spectrum sunscreen daily",
            "Avoid peak sun hours (10am-4pm)",
            "Regular skin checks after treatment",
            "Higher risk of developing additional BCCs"
        ],
        "severity": "Medium-High",
        "consultation": "Schedule dermatologist appointment within 1-2 weeks."
    },
    
    "Actinic keratoses": {
        "description": "Actinic keratoses (AK) are rough, scaly patches on the skin caused by years of sun exposure. They are considered precancerous and can develop into squamous cell carcinoma if left untreated.",
        "symptoms": [
            "Rough, dry, scaly patches",
            "Pink, red, or brown coloration",
            "Usually less than 2.5cm in diameter",
            "May feel like sandpaper",
            "Commonly on face, ears, scalp, hands",
            "May itch or burn"
        ],
        "treatment": "Treatment options include cryotherapy, topical medications (5-fluorouracil, imiquimod), photodynamic therapy, chemical peels, or laser therapy. Early treatment prevents progression to skin cancer.",
        "precautions": [
            "Consult dermatologist for treatment",
            "Minimize sun exposure",
            "Use SPF 30+ sunscreen daily",
            "Wear protective clothing and hats",
            "Regular skin examinations",
            "Monitor for changes in existing lesions"
        ],
        "severity": "Medium",
        "consultation": "Schedule dermatologist appointment within 2-4 weeks."
    },
    
    "Vascular lesions": {
        "description": "Vascular lesions are abnormalities in blood vessels that appear on the skin. They include hemangiomas, port-wine stains, cherry angiomas, and spider veins. Most are benign but some may require treatment.",
        "symptoms": [
            "Red, purple, or blue discoloration",
            "Flat or raised lesions",
            "May blanch when pressed",
            "Various sizes from tiny to large",
            "Can appear anywhere on the body"
        ],
        "treatment": "Treatment depends on the type and severity. Options include laser therapy, sclerotherapy, cryotherapy, or surgical removal. Many vascular lesions are cosmetic concerns and treatment is optional.",
        "precautions": [
            "Monitor for changes in size or color",
            "Protect from trauma (may bleed easily)",
            "Consult if lesions bleed frequently",
            "Sun protection recommended",
            "Seek medical advice if painful or rapidly growing"
        ],
        "severity": "Low-Medium",
        "consultation": "Consult for cosmetic concerns or if lesions change."
    },
    
    "Dermatofibroma": {
        "description": "Dermatofibromas are common, benign skin growths that typically appear on the legs. They are firm, small bumps that may be pink, brown, or red. They are harmless and often develop after minor injuries like insect bites.",
        "symptoms": [
            "Firm, raised bump",
            "Pink, brown, or reddish-brown color",
            "Usually 0.5-1cm in diameter",
            "Dimple sign (dimples when pinched)",
            "Commonly on lower legs",
            "May be tender or itchy"
        ],
        "treatment": "Usually no treatment needed. If bothersome or for cosmetic reasons, surgical excision is an option. Note that dermatofibromas may leave a scar when removed.",
        "precautions": [
            "Avoid picking or scratching",
            "Monitor for changes",
            "Consult if rapid growth occurs",
            "Generally harmless - no special precautions needed",
            "Seek advice if painful or bleeding"
        ],
        "severity": "Low",
        "consultation": "Non-urgent. Consult if concerned or if changes occur."
    }
}

# Disclaimer text
MEDICAL_DISCLAIMER = (
    "IMPORTANT: This AI-based prediction is for informational purposes only and should NOT be "
    "considered a medical diagnosis. Always consult with a qualified dermatologist or healthcare "
    "professional for proper medical advice, diagnosis, and treatment. Skin conditions require "
    "professional evaluation, and some may require biopsy for definitive diagnosis."
)
