from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption, MarkdownOption
from nbautoeval import TextContent, MarkdownContent


############
quiz = Quiz(

    # needs a unique name for storing progress and grades
    exoname="quiz-sample-mines",

    questions=[
        QuizQuestion(question="Lors d'un codage en bande de base :",
options=[
    Option("La fréquence des bits est du même ordre de grandeur que la fréquence du signal physique transmis",
           correct=True),
    Option("La fréquence des bits est beaucoup plus élevée que la fréquence du signal physique transmis"),
	Option("La fréquence des bits est beaucoup plus basse que la fréquence du signal physique transmis"),
    Option("La fréquence de transmission des bits varie périodiquement"),
    ],  
    horizontal_layout=True,
    score=6,
),
        
        QuizQuestion(question="Un autre layout : lors d'un codage en bande de base :",
options=[
    Option("La fréquence des bits est du même ordre de grandeur que la fréquence du signal physique transmis",
           correct=True),
    Option("La fréquence des bits est beaucoup plus élevée que la fréquence du signal physique transmis"),
    Option("La fréquence des bits est beaucoup plus basse que la fréquence du signal physique transmis"),  
    Option("La communication peut être affectée par les pertes de synchronisation", correct=True),  
    ],
    score=(6, -2),
),

        QuizQuestion(question="Lors d'un codage en modulation :",
options=[
    Option("La fréquence des bits est du même ordre de grandeur que la fréquence du signal physique transmis"),
    Option("La fréquence des bits est beaucoup plus élevée que la fréquence du signal physique transmis"),
    Option("La fréquence des bits est beaucoup plus basse que la fréquence du signal physique transmis", correct=True),
    Option("On transmet l'information grâce à la composante continue"),
    ],
    horizontal_layout=True,
    score=(6, -3, -1),
),
        
        QuizQuestion(question="Lors d'un codage en modulation :",
options=[
    Option("La fréquence des bits est du même ordre de grandeur que la fréquence du signal physique transmis"),
    Option("La fréquence des bits est beaucoup plus élevée que la fréquence du signal physique transmis"),
    Option("La fréquence des bits est beaucoup plus basse que la fréquence du signal physique transmis", correct=True),
    Option("Seule l'amplitude peut-être modulée"),
    ],
    horizontal_layout=True,
    score=6,
),
        
        QuizQuestion(question=
"""Dans un module d'intégration Verilog, lorsqu'on veut relier la sortie
d'un module sur l'entrée d'un autre, on peut utiliser :""",
options=[
    MarkdownOption("Une variable de type **wire**", correct=True),
    MarkdownOption("Une variable de type `reg`"),
    MarkdownOption("Une variable de type *parameter*"),
    MarkdownOption("Une variable de type ***localparam***"),
    MathOption(r"Une variable de type $\forall x\in\mathbb{C}$"),
    ],
    exactly_one_option=True,
    score=6,
),
        
        QuizQuestion(
    question=TextContent(
"""// clk est une entrée d'horloge
reg[1:0] a ;
reg[1:0] b ;
always @(posedge clk) begin
    if (reset) begin
        a <= 1 ;
        b <= 2 ;
    end else begin
        a <= b ;
        b <= a ;
    end
end""", is_code=True),
question2=MarkdownContent("En Verilog, le bloc `always` ci-contre :"),
options=[
    MarkdownOption("Représente un bloc de logique combinatoire d'entrées `a` et `b`"),
    Option("Est un bloc de logique séquentielle", correct=True),
    Option("Provoquera une erreur de synthèse"),
    # ici je mets un <br> à la main parce que sinon c'est moche..
    MarkdownOption("""Va intervertir `a` et `b` à chaque front montant de `clk` 
        une fois le signal `reset` passé de 1 à 0.
        <br>Lorsqu'une des valeurs sera à 1, l'autre sera à 2""",
        correct=True),
],
    horizontal_layout=True,
    score=6,
),
        
        
    ],
    
    max_attempts = 1,
)
