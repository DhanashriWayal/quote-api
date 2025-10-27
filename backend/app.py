from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# -------------------------------------------------
# FULL QUOTE DATABASE: 55 Quotes (Original 5 + 50 New)
# -------------------------------------------------
QUOTES = [
    # ORIGINAL 5
    {"content": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "tags": ["programming"]},
    {"content": "First, solve the problem. Then, write the code.", "author": "John Johnson", "tags": ["programming"]},
    {"content": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "tags": ["technology"]},
    {"content": "The best error message is the one that never shows up.", "author": "Thomas Fuchs", "tags": ["programming", "debugging"]},
    {"content": "Make it work, make it right, make it fast.", "author": "Kent Beck", "tags": ["programming"]},
    
    # NEW 50: Programming & Tech Quotes
    {"content": "Programs must be written for people to read, and only incidentally for machines to execute.", "author": "Harold Abelson", "tags": ["programming"]},
    {"content": "If the code and the comments do not match, possibly both are incorrect.", "author": "Norm Schryer", "tags": ["programming", "debugging"]},
    {"content": "Before software can be reusable it first has to be usable.", "author": "Ralph Johnson", "tags": ["programming"]},
    {"content": "If you optimize everything, you will always be unhappy.", "author": "Donald Knuth", "tags": ["programming", "technology"]},
    {"content": "Your mind is programmable – if you're not programming your mind, else will program it for you.", "author": "Jeremy Hammond", "tags": ["motivation", "programming"]},
    {"content": "To iterate is human, to recurse divine.", "author": "L. Peter Deutsch", "tags": ["programming"]},
    {"content": "Any sufficiently advanced technology is indistinguishable from magic.", "author": "Arthur C. Clarke", "tags": ["technology", "innovation"]},
    {"content": "The only way to learn a new programming language is by writing programs in it.", "author": "Dennis Ritchie", "tags": ["programming"]},
    {"content": "In programming, the hard part isn't solving problems, but deciding what problems to solve.", "author": "Paul Graham", "tags": ["programming"]},
    {"content": "No one in the brief history of computing has ever written a piece of perfect software. It's unlikely that you'll be the first.", "author": "Andy Hunt", "tags": ["programming"]},
    {"content": "It's better to wait for a productive programmer to become available than it is to wait for the first available programmer to become productive.", "author": "Unknown", "tags": ["programming"]},
    {"content": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler", "tags": ["programming"]},
    {"content": "Don't comment bad code – rewrite it.", "author": "Brian Kernighan", "tags": ["programming", "debugging"]},
    {"content": "People don't care about what you say, they care about what you build.", "author": "Mark Zuckerberg", "tags": ["technology", "innovation"]},
    {"content": "We have to stop optimizing for programmers and start optimizing for users.", "author": "Jeff Atwood", "tags": ["technology"]},
    {"content": "Coding is the language of the future, and every girl should learn it. As we depend on technology more and more every day, learning to code isn't just smart, it's necessary.", "author": "Karlie Kloss", "tags": ["motivation", "programming"]},
    {"content": "Programming isn't about what you know; it's about what you can figure out.", "author": "Andrew Hunt", "tags": ["programming"]},
    {"content": "The only thing more frightening than a programmer with a screwdriver or a hardware engineer with a program is a user with a pair of wire cutters and the root password.", "author": "Brian Reed", "tags": ["programming", "humor"]},
    {"content": "If you also think technology just automatically gets better every year but it actually doesn't.", "author": "Elon Musk", "tags": ["technology", "innovation"]},
    {"content": "Programming is just saying 'I have a meeting in an hour so better not start on this yet' to yourself until you die.", "author": "Unknown", "tags": ["programming", "humor"]},
    {"content": "Technological progress has merely provided us with more efficient means for going backwards.", "author": "Aldous Huxley", "tags": ["technology"]},
    {"content": "Once computers can program, they basically take over technological progress because already, today, the majority of technological progress is run by software, by programming.", "author": "Demis Hassabis", "tags": ["technology", "programming"]},
    {"content": "The secret of living a life of excellence is merely a matter of thinking thoughts of excellence. Really, it's a matter of programming our minds with thoughts of excellence.", "author": "Charles R. Swindoll", "tags": ["motivation"]},
    {"content": "We live in a world where finding fault in others seems to be the favorite blood sport. It has long been the basis of political campaign strategy. It is the theme of much television programming across the world.", "author": "Charles R. Swindoll", "tags": ["technology"]},
    {"content": "Studying neuro-linguistic programming is what teaches you how to implant and extract thoughts. Mixing psychology, hypnotism and magic somewhat goes into this area called mentalism, which is what I mostly do. It's magic of the mind.", "author": "Max Maven", "tags": ["programming", "innovation"]},
    {"content": "When designers replaced the command line interface with the graphical user interface, billions of people who are not programmers could make use of computer technology.", "author": "Steve Jobs", "tags": ["technology"]},
    {"content": "You could summarize everything I did at Apple was making tools to empower creative people. 'QuickDraw' empowered all these other programmers to now be able to sling stuff on the screen.", "author": "Bill Atkinson", "tags": ["programming"]},
    {"content": "I find that creative streak I think often leads in programmers to be good predictors of where culture as a whole is going to go.", "author": "Billy Corgan", "tags": ["programming", "innovation"]},
    {"content": "Most good programmers do programming not because they expect to get paid or get adulation by the public, but because it is fun to program.", "author": "Linus Torvalds", "tags": ["programming", "motivation"]},
    {"content": "If debugging is the process of removing software bugs, then programming must be the process of putting them in.", "author": "Edsger Dijkstra", "tags": ["debugging", "humor"]},
    {"content": "Measuring programming progress by lines of code is like measuring aircraft building progress by weight.", "author": "Bill Gates", "tags": ["programming"]},
    {"content": "Programming today is a race between software engineers striving to build bigger and better idiot-proof programs, and the Universe trying to produce bigger and better idiots. So far, the Universe is winning.", "author": "Rick Cook", "tags": ["programming", "humor"]},
    {"content": "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil.", "author": "C. A. R. Hoare", "tags": ["programming"]},
    {"content": "Walking on water and developing software from a specification are easy if both are frozen.", "author": "Edward V. Berard", "tags": ["programming"]},
    {"content": "It always sounds like you either have to be naive or you have to be cynical. I think the best solution is to be both.", "author": "Unknown", "tags": ["programming"]},
    {"content": "The primary duty of an exception handler is to get the error out of the lap of the programmer and into the surprised face of the user.", "author": "Verity Stob", "tags": ["debugging"]},
    {"content": "Computers are good at following instructions, but not at reading your mind.", "author": "Donald Knuth", "tags": ["programming"]},
    {"content": "The most important property of a program is whether it accomplishes the intention of its user.", "author": "C. A. R. Hoare", "tags": ["programming"]},
    {"content": "A program is never finished; it is just abandoned.", "author": "Unknown", "tags": ["programming"]},
    {"content": "The first 90% of the code accounts for the first 90% of the development time. The remaining 10% of the code accounts for the other 90% of the development time.", "author": "Tom Cargill", "tags": ["programming"]},
    {"content": "The generation of random numbers is too important to be left to chance.", "author": "Robert Coveyou", "tags": ["programming"]},
    {"content": "Most software today is very much like an Egyptian pyramid with millions of bricks piled on top of each other, with no structural integrity, but just done by brute force and thousands of slaves.", "author": "Alan Kay", "tags": ["programming"]},
    {"content": "The use of COBOL cripples the mind; its teaching should therefore be rated as a criminal offense.", "author": "Edsger Dijkstra", "tags": ["programming"]},
    {"content": "Anyone can do any amount of work provided it isn't the work he is supposed to be doing at the moment.", "author": "Robert Benchley", "tags": ["humor"]},
    {"content": "Computer science is no more about computers than astronomy is about telescopes.", "author": "Edsger Dijkstra", "tags": ["technology"]},
    {"content": "I don't care if it works on your machine! We are not shipping your machine!", "author": "Vidhu Singh", "tags": ["debugging"]},
    {"content": "C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it blows away your whole leg.", "author": "Bjarne Stroustrup", "tags": ["programming"]},
    {"content": "Perl – The only language that looks the same before and after RSA encryption.", "author": "Keith Bostic", "tags": ["programming", "humor"]},
    {"content": "There are 2 hard problems in computer science: cache invalidation, naming things, and off-by-one errors.", "author": "Leon Bambrick", "tags": ["programming"]},
    {"content": "The most disastrous thing that you can ever learn is your first programming language.", "author": "Alan Kay", "tags": ["programming"]},
    {"content": "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.", "author": "Brian Kernighan", "tags": ["debugging"]},
    {"content": "The first rule of any technology used in a business is that automation applied to an efficient operation will magnify the efficiency. The second is that automation applied to an inefficient operation will magnify the inefficiency.", "author": "Bill Gates", "tags": ["technology"]},
    {"content": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs", "tags": ["innovation"]},
    {"content": "In order to be irreplaceable one must always be different.", "author": "Coco Chanel", "tags": ["innovation"]},
    {"content": "A computer once beat a man at chess, but it was no match for a man with a mallet.", "author": "Unknown", "tags": ["technology", "humor"]},
    {"content": "The function of good software is to make the complex look simple.", "author": "Grace Hopper", "tags": ["programming"]},
    {"content": "The best way to predict the future is to invent it.", "author": "Alan Kay", "tags": ["technology"]},
    {"content": "Computers are useless: they can only give you answers.", "author": "Pablo Picasso", "tags": ["technology"]},
    {"content": "The computer was born to solve problems that did not exist before.", "author": "Bill Gates", "tags": ["technology"]},
    {"content": "The real problem is not whether machines think but whether men do.", "author": "B. F. Skinner", "tags": ["technology"]},
    {"content": "Hardware: the parts of a computer system that can be kicked.", "author": "Jeff Pesis", "tags": ["technology", "humor"]},
]

# -------------------------------------------------
# API Routes (Unchanged)
# -------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Quote API Live!",
        "endpoints": {
            "GET /random": "Get random quote (?tag=programming)",
            "GET /health": "Health check"
        },
        "total_quotes": len(QUOTES)
    })

@app.route("/random")
def random_quote():
    tag = request.args.get("tag")
    filtered = [
        q for q in QUOTES
        if not tag or any(tag.lower() in t.lower() for t in q["tags"])
    ]
    if not filtered:
        return jsonify({"error": "No quotes found for the given tag"}), 404
    return jsonify(random.choice(filtered))

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "quote-api", "total_quotes": len(QUOTES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)