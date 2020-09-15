from IPython.display import display
from ipywidgets import HTML
from markdown_it import MarkdownIt

french = """
* le quiz est contenu dans **une cellule de code**, 
  que **vous devez évaluer** pour faire **apparaitre les questions**
* toutes les questions ont **au moins une réponse valable**,  
  si vous ne cochez aucune réponse on considère que vous préférez ne pas répondre
* il y a deux sortes de questions,  
  * à **choix unique (sans ♧)** : ne peuvent avoir qu'une seul réponse valable 
  * à **choix multiple (avec ♧)** : celles ou plusieurs cases peuvent être cochées 
* **choix unique** : le barême est indiqué, par exemple `4 pts / -1 pt / 0 pt` signifie
  * 4 points pour une **bonne réponse**
  * -1 point en cas de **réponse fausse**
  * 0 point si vous ne répondez **pas du tout** (à nouveau : si vous ne cochez aucune option)
* **choix multiple** : même principe, mais le barême apparaît comme par exemple 
  `4 pts` / `??` / `-2 pts` / `0 pt`, car **la note est progressive** en fonction
  du nombre de réponses justes; dans ce cas le barême pour toutes les réponses justes 
  ici encore est de 4pts, toutes les réponses fausses vaut -2pts, et 0pt si vous ne répondez pas;  
  si dans cet exemple vous avez 2 réponses justes sur trois, votre note apparaitra comme 
  `4 pts` / **`2 pt`** / `-2 pts` / `0 pt`; et vous avez 2pts parce vous obtenez
  les deux tiers entre le min et le max des notes; 
* vous avez un nombre fixe d'essais pour répondre à un quiz - indiqué dans le bouton de soumission;  
  une fois votre nombre d'essais épuisé - ou plus tôt si vous avez tout juste -
  la correction vous montre (en rouge vif) les cases où vous vous êtes trompé ;
  les cases avec un ☛ donnent des explications supplémentaires
* le résultat final correspond à votre meilleur essai;
  les essais sont notés indépendamment les uns des autres,
   il n'y a pas d'effet cumulatif : 
   si par exemple vous obtenez 10/20 au premier essai en ayant juste à la question 1,
   et 12/20 au deuxième essai en ayant faux à la question 1,
   on retient le 12/20, la bonne réponse à l'essai #1 n'affecte pas l'essai #2
"""
  
english = """
* le quiz is contained in a **code cell**, most often empty at first, so **you need 
  to evaluate it** to get the questions to show up
* all questions have at least one valid answer;  
  if you do not tick any box in a question, it means you prefer not to answer
* there are 2 kinds of questions,  
  * **single choice (without ♧)** : can only have one valid answer
  * **multiple multiple (qith ♧)** : several boxes may be ticked
* **single choice** : the score is shown like e.g. `4 pts / -1 pt / 0 pt`, meaning 
  * 4 points for a **valid answer**
  * -1 point for a **wrong answer**
  * 0 point if you do not answer (again, if you do not tick any box)
* **multiple choice** : same idea, but the score will show like e.g. 
  `4 pts` / `??` / `-2 pts` / `0 pt`,  
  because **the grade is progressive** according 
  to the number of right answers;   
  in that example, again you'll get 4pt for all answers correct, 
  -2pts for all answers wrong, and 0pt if you prefer to opt out;  
  in this example if you have 2 correct answers out of 3, you will see  
  `4 pts` / **`2 pt`** / `-2 pts` / `0 pt`; and you get 2pts because 
  you obtain 2/3 between the min and max grades
* you have a fixed number of attempts to answer a quiz - shown in the submit button;
  once that number has run out - or earier if you get the max score -
  the correction outlines (in stark red) the boxes that you have gotten wrong;
  additional areas with a ☛ may provide additional explanation
* your final score corresponds to your best attempt; 
  attempts are independent from one another, there is no cumulative effect :  
  if for example you get 10/20 on your first attempt, with question 1 being right,
  and 12/20 on your second one with question 1 begin wrong, the second score is retained,
  the correct answer on attempt #1 does not impact attempt #2
"""



langs = {'fr': french, 'en': english}

def quiz_help(lang='en'):
    markdown = langs.get(lang, f"*no available help for lang {lang}")
    html = MarkdownIt("commonmark").render(markdown)
    display(HTML(html))
