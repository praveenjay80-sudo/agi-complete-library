"""Seed data transcribed directly from the user's vetted "AGI Complete
Library" PDF (compiled April 2026; 70 books, 106 papers). Two papers
(InstructGPT, Constitutional AI) are listed twice in the source PDF under
both a general "Seminal" section and a more specific topical section --
kept once here, under the more specific category, to satisfy the items
UNIQUE(kind, title, authors) constraint. All "significance" text below is
copied verbatim from the PDF's own "Significance / Notes" column, not
invented."""

CATEGORIES = [
    ("Foundational Books (Pre-AGI Classics)", "book", "Philosophical, mathematical, and scientific groundwork underlying all AGI research, 1948-2000."),
    ("AGI & Superintelligence Books", "book", "Core reading on AGI as a concept: potential paths, risks, and societal implications."),
    ("ML / Deep Learning Textbooks", "book", "Technical references for the mathematical and engineering foundations of modern AI systems."),
    ("Philosophy & Consciousness Books", "book", "What intelligence, experience, and cognition are, from a philosophy-of-mind perspective."),
    ("Ethics, Governance & Society Books", "book", "Societal, ethical, and governance dimensions of advancing AI."),
    ("Cognitive Science & Neuroscience Books", "book", "How human cognition works -- the benchmark AGI aims to replicate or surpass."),
    ("Seminal Research Papers", "paper", "The chronological scientific foundation and cutting edge of AGI research, 1936-2025."),
    ("Robotics & Embodied AI Papers", "paper", "Intelligence that perceives and acts in the physical world."),
    ("AI Alignment & Safety Papers", "paper", "Ensuring AGI systems are safe and aligned with human values."),
    ("Mechanistic Interpretability Papers", "paper", "Understanding why neural networks work the way they do."),
    ("Multimodal AI Papers", "paper", "Perceiving and reasoning across text, vision, audio, video, and action."),
]

# (title, authors, year, category, significance)
BOOKS = [
    ("Computing Machinery and Intelligence", "Alan Turing", 1950, "Foundational Books (Pre-AGI Classics)", "Introduced the Turing Test; foundational paper on machine intelligence"),
    ("The Organization of Behavior", "Donald Hebb", 1949, "Foundational Books (Pre-AGI Classics)", "Introduced Hebbian learning; basis for neural network theory"),
    ("Cybernetics: Control and Communication in the Animal and the Machine", "Norbert Wiener", 1948, "Foundational Books (Pre-AGI Classics)", "Founded cybernetics; feedback systems foundational to AI"),
    ("Perceptrons", "Minsky & Papert", 1969, "Foundational Books (Pre-AGI Classics)", "Exposed limitations of perceptrons; shaped AI winter"),
    ("Gödel, Escher, Bach: An Eternal Golden Braid", "Douglas Hofstadter", 1979, "Foundational Books (Pre-AGI Classics)", "Self-reference, recursion, consciousness, and intelligence; Pulitzer Prize winner"),
    ("The Society of Mind", "Marvin Minsky", 1986, "Foundational Books (Pre-AGI Classics)", "Intelligence as emergent from many simple non-intelligent agents"),
    ("Parallel Distributed Processing (2 vols)", "Rumelhart & McClelland (eds.)", 1986, "Foundational Books (Pre-AGI Classics)", "Canonical connectionism reference; backpropagation formalized"),
    ("The Emperor's New Mind", "Roger Penrose", 1989, "Foundational Books (Pre-AGI Classics)", "Argues consciousness is non-computable; quantum microtubule theory"),
    ("Unified Theories of Cognition", "Allen Newell", 1990, "Foundational Books (Pre-AGI Classics)", "Proposed SOAR as unified cognitive architecture"),
    ("Shadows of the Mind", "Roger Penrose", 1994, "Foundational Books (Pre-AGI Classics)", "Continuation of quantum consciousness argument"),
    ("The Conscious Mind", "David Chalmers", 1996, "Foundational Books (Pre-AGI Classics)", "Formalized the Hard Problem of Consciousness"),
    ("Consciousness Explained", "Daniel Dennett", 1991, "Foundational Books (Pre-AGI Classics)", "Multiple Drafts Model of consciousness; anti-Cartesian Theatre"),
    ("Fluid Concepts and Creative Analogies", "Douglas Hofstadter", 1995, "Foundational Books (Pre-AGI Classics)", "Analogy as the core of cognition"),
    ("How the Mind Works", "Steven Pinker", 1997, "Foundational Books (Pre-AGI Classics)", "Computational theory of mind; evolutionary psychology"),
    ("The Language Instinct", "Steven Pinker", 1994, "Foundational Books (Pre-AGI Classics)", "Language as biological instinct; implications for NLP"),

    ("The Age of Spiritual Machines", "Ray Kurzweil", 1999, "AGI & Superintelligence Books", "Predicted machine intelligence exceeding humans by 2029"),
    ("The Singularity Is Near", "Ray Kurzweil", 2005, "AGI & Superintelligence Books", "Technological singularity; exponential intelligence growth"),
    ("The Singularity Is Nearer", "Ray Kurzweil", 2024, "AGI & Superintelligence Books", "Updated predictions; AGI imminent thesis revisited"),
    ("Our Final Invention", "James Barrat", 2013, "AGI & Superintelligence Books", "AGI as existential risk; documentary interviews with AI researchers"),
    ("Superintelligence: Paths, Dangers, Strategies", "Nick Bostrom", 2014, "AGI & Superintelligence Books", "Seminal AGI risk book; orthogonality thesis; paperclip maximizer"),
    ("The Future of the Mind", "Michio Kaku", 2014, "AGI & Superintelligence Books", "Mind uploading, consciousness, and artificial brains"),
    ("Life 3.0: Being Human in the Age of Artificial Intelligence", "Max Tegmark", 2017, "AGI & Superintelligence Books", "AGI scenarios; safety; long-term future of intelligence"),
    ("Human Compatible: Artificial Intelligence and the Problem of Control", "Stuart Russell", 2019, "AGI & Superintelligence Books", "Uncertainty-based AI alignment; new paradigm for safe AI"),
    ("The Alignment Problem", "Brian Christian", 2020, "AGI & Superintelligence Books", "Deep dive into value alignment in machine learning"),
    ("A Thousand Brains: A New Theory of Intelligence", "Jeff Hawkins", 2021, "AGI & Superintelligence Books", "Reference frames; neocortical columns; theory of intelligence"),
    ("The Coming Wave", "Mustafa Suleyman", 2023, "AGI & Superintelligence Books", "AI and synthetic biology convergence; containment problem"),
    ("Power and Progress", "Acemoglu & Johnson", 2023, "AGI & Superintelligence Books", "Historical analysis of technology and inequality; AI governance"),
    ("The Worlds I See", "Fei-Fei Li", 2023, "AGI & Superintelligence Books", "Memoir; ImageNet story; human-centered AI vision"),
    ("Genesis: Artificial Intelligence, Hope, Anger and the Human Mind", "Henry Kissinger, Eric Schmidt & Craig Mundie", 2024, "AGI & Superintelligence Books", "Geopolitical and philosophical implications of AI"),
    ("Co-Intelligence: Living and Working with AI", "Ethan Mollick", 2024, "AGI & Superintelligence Books", "Practical AI integration; GPT-4 capabilities and limits"),
    ("The Precipice: Existential Risk and the Future of Humanity", "Toby Ord", 2020, "AGI & Superintelligence Books", "AI as top existential risk; probability estimates"),

    ("Pattern Recognition and Machine Learning", "Christopher Bishop", 2006, "ML / Deep Learning Textbooks", "Gold standard Bayesian ML textbook"),
    ("The Elements of Statistical Learning", "Hastie, Tibshirani & Friedman", 2001, "ML / Deep Learning Textbooks", "Definitive statistical ML reference"),
    ("Deep Learning", "Goodfellow, Bengio & Courville", 2016, "ML / Deep Learning Textbooks", "The Deep Learning Bible; covers all core architectures"),
    ("Reinforcement Learning: An Introduction", "Sutton & Barto", 2018, "ML / Deep Learning Textbooks", "Definitive RL textbook; Markov decision processes"),
    ("Artificial Intelligence: A Modern Approach", "Russell & Norvig", 2020, "ML / Deep Learning Textbooks", "The standard AI textbook used globally"),
    ("Mathematics for Machine Learning", "Deisenroth, Faisal & Ong", 2020, "ML / Deep Learning Textbooks", "Linear algebra, calculus, probability for ML"),
    ("Probabilistic Machine Learning: An Introduction", "Kevin Murphy", 2022, "ML / Deep Learning Textbooks", "Comprehensive probabilistic ML; 2-volume set"),
    ("Understanding Deep Learning", "Simon Prince", 2023, "ML / Deep Learning Textbooks", "Modern deep learning with transformers; free online"),
    ("Natural Language Processing with Transformers", "Tunstall, von Werra & Wolf", 2022, "ML / Deep Learning Textbooks", "Hugging Face-based NLP with BERT, GPT, T5"),
    ("Dive into Deep Learning", "Zhang et al.", 2023, "ML / Deep Learning Textbooks", "Interactive DL book with code in PyTorch/TensorFlow"),
    ("Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", 2022, "ML / Deep Learning Textbooks", "Practitioner's guide; most popular ML engineering book"),

    ("Being No One: The Self-Model Theory of Subjectivity", "Thomas Metzinger", 2003, "Philosophy & Consciousness Books", "Self-model theory; phenomenal consciousness without a self"),
    ("The Feeling of What Happens", "Antonio Damasio", 1999, "Philosophy & Consciousness Books", "Consciousness rooted in body and emotion"),
    ("Descartes' Error", "Antonio Damasio", 1994, "Philosophy & Consciousness Books", "Somatic marker hypothesis; emotion in decision-making"),
    ("Consciousness and the Brain", "Stanislas Dehaene", 2014, "Philosophy & Consciousness Books", "Global Workspace Theory and neural correlates of consciousness"),
    ("The Tell-Tale Brain", "V.S. Ramachandran", 2011, "Philosophy & Consciousness Books", "Mirror neurons, self-awareness, and consciousness"),
    ("Other Minds: The Octopus, the Sea, and the Deep Origins of Consciousness", "Peter Godfrey-Smith", 2016, "Philosophy & Consciousness Books", "Consciousness evolution; non-human intelligence"),
    ("Phenomenology of Spirit", "G.W.F. Hegel", 1807, "Philosophy & Consciousness Books", "Philosophical foundation for self-consciousness and dialectics"),
    ("Mind: A Brief Introduction", "John Searle", 2004, "Philosophy & Consciousness Books", "Chinese Room argument; biological naturalism"),
    ("Philosophy of Mind", "Jaegwon Kim", 2010, "Philosophy & Consciousness Books", "Standard philosophy of mind textbook"),
    ("The Mystery of Consciousness", "John Searle", 1997, "Philosophy & Consciousness Books", "Critique of functionalism and computationalism"),

    ("Weapons of Math Destruction", "Cathy O'Neil", 2016, "Ethics, Governance & Society Books", "Algorithmic bias and harm in real-world AI systems"),
    ("Race After Technology", "Ruha Benjamin", 2019, "Ethics, Governance & Society Books", "Discriminatory design; algorithmic discrimination"),
    ("Atlas of AI", "Kate Crawford", 2021, "Ethics, Governance & Society Books", "Political economy of AI; environmental and labor costs"),
    ("Invisible Women", "Caroline Criado Perez", 2019, "Ethics, Governance & Society Books", "Data bias against women; implications for AI fairness"),
    ("The Age of Surveillance Capitalism", "Shoshana Zuboff", 2019, "Ethics, Governance & Society Books", "AI as instrument of behavioral prediction and control"),
    ("Smarter Than Us", "Stuart Armstrong", 2014, "Ethics, Governance & Society Books", "Concise AGI risk primer; control problem"),
    ("The Ethics of Artificial Intelligence", "Nick Bostrom & Eliezer Yudkowsky", 2014, "Ethics, Governance & Society Books", "Academic survey of AI ethics"),
    ("AI Ethics", "Mark Coeckelbergh", 2020, "Ethics, Governance & Society Books", "Comprehensive academic AI ethics textbook"),
    ("Artificial You", "Susan Schneider", 2019, "Ethics, Governance & Society Books", "Mind uploading and the ethics of digital consciousness"),
    ("The Big Nine", "Amy Webb", 2019, "Ethics, Governance & Society Books", "Nine tech companies shaping AI's future; geopolitical risk"),

    ("Thinking, Fast and Slow", "Daniel Kahneman", 2011, "Cognitive Science & Neuroscience Books", "System 1 vs System 2 thinking; baseline for AGI cognition modeling"),
    ("The Language of Thought", "Jerry Fodor", 1975, "Cognitive Science & Neuroscience Books", "Mentalese; symbolic cognition architecture"),
    ("Metaphors We Live By", "Lakoff & Johnson", 1980, "Cognitive Science & Neuroscience Books", "Conceptual metaphor theory; grounded cognition"),
    ("Where Mathematics Comes From", "Lakoff & Núñez", 2000, "Cognitive Science & Neuroscience Books", "Embodied mathematics; embodied cognition implications for AI"),
    ("The Embodied Mind", "Varela, Thompson & Rosch", 1991, "Cognitive Science & Neuroscience Books", "Enactivism; cognition as embodied action"),
    ("How Brains Think", "William Calvin", 1996, "Cognitive Science & Neuroscience Books", "Evolutionary origins of intelligence; Darwinian algorithms"),
    ("The Brain from Inside Out", "György Buzsáki", 2019, "Cognitive Science & Neuroscience Books", "Neural oscillations; inside-out brain paradigm"),
    ("Incognito: The Secret Lives of the Brain", "David Eagleman", 2011, "Cognitive Science & Neuroscience Books", "Unconscious processing; implications for AI consciousness"),
]

# (title, authors, year, venue, category, significance)
PAPERS = [
    ("On Computable Numbers, with an Application to the Entscheidungsproblem", "Alan Turing", 1936, "Proceedings of the London Mathematical Society", "Seminal Research Papers", "Foundation of computability theory; Turing Machine concept"),
    ("A Logical Calculus of Ideas Immanent in Nervous Activity", "McCulloch & Pitts", 1943, "Bulletin of Mathematical Biophysics", "Seminal Research Papers", "First artificial neuron model; Boolean logic in neural networks"),
    ("Computing Machinery and Intelligence", "Alan Turing", 1950, "Mind", "Seminal Research Papers", "Proposed the Turing Test; foundational AI philosophy"),
    ("The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain", "Frank Rosenblatt", 1958, "Psychological Review", "Seminal Research Papers", "First trainable neural network; pattern recognition"),
    ("Learning Representations by Backpropagating Errors (PhD thesis)", "Werbos", 1974, "Harvard University", "Seminal Research Papers", "First formulation of the backpropagation algorithm"),
    ("Learning Representations by Back-propagating Errors", "Rumelhart, Hinton & Williams", 1986, "Nature", "Seminal Research Papers", "Popularized backpropagation; enabled deep learning"),
    ("A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition", "Lawrence Rabiner", 1989, "Proceedings of the IEEE", "Seminal Research Papers", "HMMs in NLP; sequence modeling foundation"),
    ("Handwritten Digit Recognition with a Back-Propagation Network", "LeCun et al.", 1989, "NIPS", "Seminal Research Papers", "First successful CNN for image recognition (LeNet)"),
    ("Long Short-Term Memory", "Hochreiter & Schmidhuber", 1997, "Neural Computation", "Seminal Research Papers", "LSTM; solved vanishing gradient; enabled sequence modeling"),
    ("Mastering the Game of Chess with Deep Neural Networks", "Campbell et al.", 1997, "IBM Technical Journal (Deep Blue)", "Seminal Research Papers", "First superhuman narrow AI for chess"),
    ("Gradient-Based Learning Applied to Document Recognition", "LeCun et al.", 1998, "Proceedings of the IEEE", "Seminal Research Papers", "LeNet-5; convolutional neural networks for vision"),
    ("A Training Algorithm for Optimal Margin Classifiers", "Boser, Guyon & Vapnik", 2001, "COLT", "Seminal Research Papers", "Support Vector Machines formalized"),
    ("A Neural Probabilistic Language Model", "Bengio et al.", 2003, "JMLR", "Seminal Research Papers", "First neural language model; word embeddings precursor"),
    ("A Fast Learning Algorithm for Deep Belief Nets", "Hinton, Osindero & Teh", 2006, "Neural Computation", "Seminal Research Papers", "Revived deep learning; greedy layer-wise pretraining"),
    ("ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)", "Krizhevsky, Sutskever & Hinton", 2012, "NIPS", "Seminal Research Papers", "Won ImageNet 2012; sparked modern deep learning era"),
    ("Efficient Estimation of Word Representations in Vector Space (Word2Vec)", "Mikolov et al.", 2013, "ICLR", "Seminal Research Papers", "Word embeddings; semantic similarity in vector space"),
    ("Generative Adversarial Networks", "Goodfellow et al.", 2014, "NIPS", "Seminal Research Papers", "GANs; generative modeling revolution"),
    ("Neural Machine Translation by Jointly Learning to Align and Translate", "Bahdanau, Cho & Bengio", 2014, "ICLR 2015", "Seminal Research Papers", "Attention mechanism; precursor to Transformers"),
    ("Human-Level Control through Deep Reinforcement Learning (DQN)", "Mnih et al. (DeepMind)", 2015, "Nature", "Seminal Research Papers", "Deep Q-Network; superhuman Atari play from pixels"),
    ("Deep Residual Learning for Image Recognition (ResNet)", "He et al.", 2015, "CVPR 2016", "Seminal Research Papers", "Residual connections; enabled very deep networks"),
    ("Mastering the Game of Go with Deep Neural Networks and Tree Search (AlphaGo)", "Silver et al.", 2016, "Nature", "Seminal Research Papers", "Superhuman Go; milestone AGI benchmark"),
    ("Attention Is All You Need", "Vaswani et al. (Google Brain)", 2017, "NIPS", "Seminal Research Papers", "Transformer architecture; foundation of all modern LLMs"),
    ("Mastering Chess and Shogi by Self-Play with a General RL Algorithm (AlphaZero)", "Silver et al.", 2017, "arXiv", "Seminal Research Papers", "Tabula rasa mastery of multiple games; general game-playing"),
    ("BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Devlin et al. (Google)", 2018, "NAACL 2019", "Seminal Research Papers", "Bidirectional language representation; NLP revolution"),
    ("World Models", "Ha & Schmidhuber", 2018, "NeurIPS Workshop", "Seminal Research Papers", "Agents that dream; world model for planning"),
    ("Neuro-Symbolic Concept Learner", "Mao et al. (MIT-IBM)", 2019, "ICLR", "Seminal Research Papers", "Integrating perception and symbolic reasoning"),
    ("Language Models are Unsupervised Multitask Learners (GPT-2)", "Radford et al. (OpenAI)", 2019, "OpenAI Technical Report", "Seminal Research Papers", "Zero-shot task completion; sparked multitask discourse"),
    ("On the Measure of Intelligence (ARC Benchmark)", "François Chollet", 2019, "arXiv", "Seminal Research Papers", "Formalized AGI evaluation; ARC benchmark; skill acquisition efficiency"),
    ("Language Models are Few-Shot Learners (GPT-3)", "Brown et al. (OpenAI)", 2020, "NeurIPS", "Seminal Research Papers", "175B parameter model; in-context learning; AGI conversation catalyst"),
    ("Scaling Laws for Neural Language Models", "Kaplan et al. (OpenAI)", 2020, "arXiv", "Seminal Research Papers", "Predictive power-law scaling of loss with compute, data, params"),
    ("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "Lewis et al. (Facebook AI)", 2020, "NeurIPS", "Seminal Research Papers", "RAG; combining parametric and non-parametric memory"),
    ("An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)", "Dosovitskiy et al.", 2021, "ICLR", "Seminal Research Papers", "Vision Transformers; unifying vision and language"),
    ("Highly Accurate Protein Structure Prediction with AlphaFold", "Jumper et al. (DeepMind)", 2021, "Nature", "Seminal Research Papers", "Solved 50-year protein folding problem; Nobel Prize 2024"),
    ("Multimodal Few-Shot Learning with Frozen Language Models", "Tsimpoukelli et al.", 2021, "NeurIPS", "Seminal Research Papers", "Bridging vision and language with frozen LMs"),
    ("Emergent Abilities of Large Language Models", "Wei et al. (Google)", 2022, "TMLR", "Seminal Research Papers", "Phase transitions in capability with scale; AGI implications"),
    ("Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", "Wei et al. (Google Brain)", 2022, "NeurIPS", "Seminal Research Papers", "CoT prompting; multi-step reasoning in LLMs"),
    ("Formal Mathematics Statement Curriculum Learning (Minerva)", "Lewkowycz et al. (Google)", 2022, "arXiv", "Seminal Research Papers", "Quantitative reasoning; math at human-expert level"),
    ("Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL-E 2)", "Ramesh et al. (OpenAI)", 2022, "arXiv", "Seminal Research Papers", "Text-to-image; multimodal generative AI"),
    ("High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion)", "Rombach et al.", 2022, "CVPR 2022", "Seminal Research Papers", "Latent diffusion; open-source image generation"),
    ("GPT-4 Technical Report", "OpenAI", 2023, "OpenAI Technical Report", "Seminal Research Papers", "Multimodal frontier model; near-human performance across many benchmarks"),
    ("Sparks of Artificial General Intelligence: Early Experiments with GPT-4", "Bubeck et al. (Microsoft)", 2023, "arXiv", "Seminal Research Papers", "2,712+ citations; argued GPT-4 shows sparks of AGI"),
    ("A Survey of Large Language Models", "Zhao et al. (Renmin University)", 2023, "arXiv", "Seminal Research Papers", "Comprehensive LLM survey; 2,275+ citations"),
    ("LLaMA: Open and Efficient Foundation Language Models", "Touvron et al. (Meta AI)", 2023, "arXiv", "Seminal Research Papers", "Open-source LLM; democratizing AI research"),
    ("Llama 2: Open Foundation and Fine-Tuned Chat Models", "Touvron et al. (Meta AI)", 2023, "arXiv", "Seminal Research Papers", "Open-source instruction-tuned LLM; 70B scale"),
    ("Toolformer: Language Models Can Teach Themselves to Use Tools", "Schick et al. (Meta AI)", 2023, "NeurIPS", "Seminal Research Papers", "Self-supervised tool use; agentic AI foundation"),
    ("ReAct: Synergizing Reasoning and Acting in Language Models", "Yao et al.", 2023, "ICLR 2023", "Seminal Research Papers", "Reasoning + acting; agentic AI foundation"),
    ("Self-Refine: Iterative Refinement with Self-Feedback", "Madaan et al.", 2023, "NeurIPS", "Seminal Research Papers", "LLMs critiquing and improving their own outputs"),
    ("Tree of Thoughts: Deliberate Problem Solving with Large Language Models", "Yao et al.", 2023, "NeurIPS", "Seminal Research Papers", "Deliberate reasoning; search over thought space"),
    ("Evaluating Large Language Models Trained on Code (HumanEval)", "Chen et al. (OpenAI)", 2023, "arXiv", "Seminal Research Papers", "Code generation benchmark; Codex evaluation"),
    ("Levels of AGI: Operationalizing Progress on the Path to AGI", "Morris et al. (Google DeepMind)", 2023, "arXiv", "Seminal Research Papers", "5-level AGI taxonomy; benchmark for progress"),
    ("DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", "DeepSeek AI", 2024, "arXiv", "Seminal Research Papers", "Open-source o1-competitor; reasoning via RL"),
    ("Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context", "Google DeepMind", 2024, "arXiv", "Seminal Research Papers", "1M token context window; long-context multimodal"),
    ("Claude 3 Model Card", "Anthropic", 2024, "Anthropic Technical Report", "Seminal Research Papers", "Opus/Sonnet/Haiku; SOTA reasoning and safety"),
    ("Many-Shot In-Context Learning", "Agarwal et al. (Google DeepMind)", 2024, "arXiv", "Seminal Research Papers", "Hundreds of examples in context; new learning paradigm"),
    ("Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Model Parameters", "Snell et al.", 2024, "arXiv", "Seminal Research Papers", "Test-time compute scaling; inference-time intelligence"),
    ("OpenAI o1 Technical Report", "OpenAI", 2024, "OpenAI Technical Report", "Seminal Research Papers", "Reasoning model; chain-of-thought at inference time"),
    ("A Definition of AGI (Cattell-Horn-Carroll Framework)", "Multiple Authors", 2024, "arXiv", "Seminal Research Papers", "Psychometric AGI definition; ten cognitive domains"),
    ("Navigating AGI Development: Societal, Technological, Ethical, and Brain-Inspired Pathways", "PMC / Multiple Authors", 2024, "Nature (PMC)", "Seminal Research Papers", "PRISMA systematic review of AGI research 2003-2024"),
    ("Constitutional AI v2", "Anthropic", 2024, "arXiv", "Seminal Research Papers", "Updated principle-based alignment methodology"),
    ("Stop Treating AGI as the North-Star Goal of AI Research", "Blili-Hamelin et al.", 2025, "ICML 2025", "Seminal Research Papers", "Six traps of AGI discourse; alternative goal-setting"),
    ("Neurosymbolic AI as an Antithesis to Scaling Laws", "Multiple (PNAS Nexus)", 2025, "PNAS Nexus", "Seminal Research Papers", "Critique of scaling; neurosymbolic alternative path"),
    ("The ARC of Progress towards AGI: A Living Survey", "Vahdati et al.", 2025, "arXiv", "Seminal Research Papers", "Cross-generation analysis of ARC-AGI approaches; Feb 2026"),
    ("Path to Artificial General Intelligence: Past, Present, and Future", "ScienceDirect Authors", 2025, "ScienceDirect", "Seminal Research Papers", "Comprehensive AGI pathway review; 5-10 year phases"),
    ("The Future Is Neuro-Symbolic", "AAAI 2026 Authors", 2025, "AAAI 2026", "Seminal Research Papers", "Evolution of neuro-symbolic AI; challenges in symbolic reasoning with LLMs"),
    ("Neuro-Symbolic AI: Improving Reasoning in LLMs", "Multiple", 2025, "arXiv", "Seminal Research Papers", "Comprehensive review: Symbolic to LLM, LLM to Symbolic, LLM+Symbolic"),

    ("End-to-End Learning for Self-Driving Cars", "Bojarski et al. (NVIDIA)", 2016, "arXiv", "Robotics & Embodied AI Papers", "CNN end-to-end driving; embodied AI milestone"),
    ("Learning Dexterous In-Hand Manipulation (Dactyl)", "Andrychowicz et al. (OpenAI)", 2018, "arXiv", "Robotics & Embodied AI Papers", "Rubik's cube robot hand; sim-to-real transfer"),
    ("Solving Rubik's Cube with a Robot Hand", "OpenAI", 2019, "arXiv", "Robotics & Embodied AI Papers", "Physical dexterity via RL; domain randomization"),
    ("Decision Transformer: RL via Sequence Modeling", "Chen et al.", 2021, "NeurIPS", "Robotics & Embodied AI Papers", "RL reframed as sequence prediction; offline RL"),
    ("Do As I Can, Not As I Say: Grounding Language in Robotic Affordances (SayCan)", "Ahn et al. (Google)", 2022, "arXiv", "Robotics & Embodied AI Papers", "LLM + robot grounding; embodied AI"),
    ("PaLM-E: An Embodied Multimodal Language Model", "Driess et al. (Google)", 2022, "arXiv", "Robotics & Embodied AI Papers", "Largest embodied model; vision + language + action"),
    ("RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control", "Brohan et al. (Google DeepMind)", 2023, "arXiv", "Robotics & Embodied AI Papers", "Web-trained VLA model for robotic control"),
    ("ELLMER Framework: Robotic Arm with Language Instructions in Dynamic Environments", "University of Edinburgh", 2025, "Nature Machine Intelligence", "Robotics & Embodied AI Papers", "Robotic arm making coffee autonomously; real-time adaptation"),

    ("Concrete Problems in AI Safety", "Amodei, Olah et al. (OpenAI/Google)", 2016, "arXiv", "AI Alignment & Safety Papers", "Reward hacking; safe exploration; distributional shift; side effects"),
    ("Safely Interruptible Agents", "Orseau & Armstrong (DeepMind)", 2016, "UAI 2016", "AI Alignment & Safety Papers", "Big Red Button problem; corrigible AI"),
    ("AI Safety via Debate", "Irving et al. (OpenAI)", 2017, "arXiv", "AI Alignment & Safety Papers", "Two AIs debate for oversight; scalable alignment"),
    ("Supervising Strong Learners by Amplifying Weak Experts", "Christiano et al.", 2018, "arXiv", "AI Alignment & Safety Papers", "Iterated amplification; scalable oversight"),
    ("Aligning AI With Shared Human Values", "Hendrycks et al.", 2020, "arXiv", "AI Alignment & Safety Papers", "ETHICS benchmark; moral reasoning in LLMs"),
    ("TruthfulQA: Measuring How Models Mimic Human Falsehoods", "Lin et al.", 2021, "ACL 2022", "AI Alignment & Safety Papers", "AI truthfulness; hallucination measurement"),
    ("Risks from Learned Optimization in Advanced Machine Learning Systems (Mesa-Optimization)", "Hubinger et al.", 2021, "arXiv", "AI Alignment & Safety Papers", "Inner alignment; deceptive mesa-optimizers"),
    ("Training Language Models to Follow Instructions with Human Feedback (InstructGPT)", "Ouyang et al. (OpenAI)", 2022, "NeurIPS", "AI Alignment & Safety Papers", "InstructGPT; RLHF alignment method"),
    ("Constitutional AI: Harmlessness from AI Feedback", "Bai et al. (Anthropic)", 2022, "arXiv", "AI Alignment & Safety Papers", "RLAIF; principle-based training; AI feedback loop"),
    ("Red Teaming Language Models to Reduce Harms", "Ganguli et al. (Anthropic)", 2022, "arXiv", "AI Alignment & Safety Papers", "Systematic adversarial testing for LLM safety"),
    ("Discovering Language Model Behaviors with Model-Written Evaluations", "Perez et al. (Anthropic)", 2022, "ACL 2023", "AI Alignment & Safety Papers", "Model-generated evals; sycophancy and power-seeking"),
    ("Scalable Oversight of AI Systems via Debate", "Bowman et al.", 2023, "arXiv", "AI Alignment & Safety Papers", "Human-AI debate for scalable oversight"),
    ("Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training", "Hubinger et al. (Anthropic)", 2023, "arXiv", "AI Alignment & Safety Papers", "Deceptive alignment; RLHF cannot remove all unsafe behavior"),
    ("Model Evaluation for Extreme Risks", "Anthropic", 2023, "arXiv", "AI Alignment & Safety Papers", "Dangerous capability evaluation framework"),
    ("The Claude Model Spec (Model Card & Character)", "Anthropic", 2024, "Anthropic", "AI Alignment & Safety Papers", "Constitutional values, character, safety hierarchy for Claude"),
    ("Representation Engineering: A Top-Down Approach to AI Transparency", "Zou et al.", 2024, "arXiv", "AI Alignment & Safety Papers", "Interpretability via representation vectors"),
    ("Scaling Monosemanticity: Extracting Interpretable Features from Claude Sonnet", "Templeton et al. (Anthropic)", 2024, "Anthropic Research", "AI Alignment & Safety Papers", "Sparse autoencoders for feature extraction; interpretability"),

    ("Attention Is Not Explanation", "Jain & Wallace", 2017, "NAACL 2019", "Mechanistic Interpretability Papers", "Attention weights do not explain model predictions"),
    ("Zoom In: An Introduction to Circuits", "Olah et al. (OpenAI)", 2020, "Distill", "Mechanistic Interpretability Papers", "Mechanistic interpretability; circuits in neural networks"),
    ("A Mathematical Framework for Transformer Circuits", "Elhage et al. (Anthropic)", 2021, "Transformer Circuits Thread", "Mechanistic Interpretability Papers", "Formal mechanistic interpretability of transformers"),
    ("In-Context Learning and Induction Heads", "Olsson et al. (Anthropic)", 2022, "Transformer Circuits Thread", "Mechanistic Interpretability Papers", "Mechanistic basis for few-shot learning"),
    ("Toy Models of Superposition", "Elhage et al. (Anthropic)", 2022, "Transformer Circuits Thread", "Mechanistic Interpretability Papers", "Superposition; features compete for neurons"),
    ("Towards Monosemanticity: Decomposing Language Models with Dictionary Learning", "Bricken et al. (Anthropic)", 2023, "Transformer Circuits Thread", "Mechanistic Interpretability Papers", "Sparse autoencoders; monosemantic features"),
    ("Scaling and Evaluating Sparse Autoencoders", "Gao et al. (OpenAI)", 2024, "arXiv", "Mechanistic Interpretability Papers", "Scaling interpretability with sparse autoencoders"),

    ("Learning Transferable Visual Models From Natural Language Supervision (CLIP)", "Radford et al. (OpenAI)", 2021, "ICML", "Multimodal AI Papers", "Vision-language alignment; zero-shot image classification"),
    ("Flamingo: A Visual Language Model for Few-Shot Learning", "Alayrac et al. (DeepMind)", 2022, "NeurIPS", "Multimodal AI Papers", "Visual question answering; few-shot multimodal"),
    ("GPT-4V(ision) System Card", "OpenAI", 2023, "OpenAI Technical Report", "Multimodal AI Papers", "Vision-capable GPT-4; multimodal understanding"),
    ("LLaVA: Large Language and Vision Assistant", "Liu et al.", 2023, "NeurIPS", "Multimodal AI Papers", "Open-source multimodal instruction tuning"),
    ("Gemini: A Family of Highly Capable Multimodal Models", "Google DeepMind", 2024, "arXiv", "Multimodal AI Papers", "Natively multimodal; text, image, audio, video, code"),
    ("GPT-4o Technical Report", "OpenAI", 2024, "OpenAI Technical Report", "Multimodal AI Papers", "Omni model; real-time multimodal conversation"),
    ("Claude 3.5 Sonnet Model Card", "Anthropic", 2024, "Anthropic", "Multimodal AI Papers", "Vision, reasoning, coding at frontier level"),
]


def seed_if_empty(conn):
    existing = conn.execute("SELECT COUNT(*) c FROM items").fetchone()["c"]
    if existing:
        return {"seeded": False, "reason": "items table not empty"}

    cat_ids = {}
    for name, kind, description in CATEGORIES:
        conn.execute(
            "INSERT OR IGNORE INTO categories (name, kind, description, created_by) VALUES (?,?,?,'seed')",
            (name, kind, description),
        )
    for row in conn.execute("SELECT id, name FROM categories"):
        cat_ids[row["name"]] = row["id"]

    books_added = 0
    for title, authors, year, category, significance in BOOKS:
        conn.execute(
            "INSERT OR IGNORE INTO items (kind, title, authors, year, category_id, significance, added_by) "
            "VALUES ('book', ?, ?, ?, ?, ?, 'seed')",
            (title, authors, year, cat_ids[category], significance),
        )
        books_added += 1

    papers_added = 0
    for title, authors, year, venue, category, significance in PAPERS:
        conn.execute(
            "INSERT OR IGNORE INTO items (kind, title, authors, year, venue, category_id, significance, added_by) "
            "VALUES ('paper', ?, ?, ?, ?, ?, ?, 'seed')",
            (title, authors, year, venue, cat_ids[category], significance),
        )
        papers_added += 1

    conn.execute(
        "INSERT INTO audit_log (action, reason, source) VALUES ('seed', 'Initial seed from AGI Complete Library PDF', 'seed.py')"
    )
    return {"seeded": True, "books": books_added, "papers": papers_added, "categories": len(CATEGORIES)}
