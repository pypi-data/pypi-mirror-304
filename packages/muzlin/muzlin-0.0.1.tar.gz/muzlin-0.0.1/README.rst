########
 Muzlin
########

*When a filter cloth 🏳️ is needed rather than a simple RAG 🏴‍☠*

*************
 What is it?
*************

Muzlin merges classical ML techniques with complex generative AI. It's
goal is to apply simple, efficent, and effective methods for filtering
many aspects of the generative text process train. These methods address
the following questions:

-  Does a RAG/GraphRAG have any context to answer the user's question?

-  Does the retrieved context contain good candidates to provide a
   complete answer (e.g. are the retrieved context too dense/sparse)?

-  Does the generated LLM response deviate from the provided context?
   (Hallucination)

-  Given a collection of questions, should an extracted portion of text
   be added to an existing RAG with respect to its ability to answer any
   of the questions in the collection?

-  Given an existing RAG, what is the probability that a new portion of
   text belongs to the RAG cluster?

-  Given a collection of embedded text (e.g. context, user question and
   answers, synthetic generated data, etc...), what components are
   considered inliers and outliers?

Muzlin is dynamic and production ready and can be added as a
decision-making layer for any LLM and agentic process flows.

**Note** while Muzlin is production ready, it is still in a development
phase and is subject to significant changes!

************
 Quickstart
************

To get started use **pip** for installation:

.. code:: bash

   pip install muzlin

In order to compared text, we need to first create a base of
information. To do this we need a collection of text embeddings:

.. code:: python

   import numpy as np
   from muzlin.encoders import HuggingFaceEncoder

   encoder = HuggingFaceEncoder()

   vectors = encoder(texts) # where texts is a list of str
   vectors = np.array(vectors)
   np.save('vectors', vectors)

Next we will construct an unsupervised anomaly detection model using the
embedded vectors:

.. code:: python

   import mlflow as ml # optional
   from muzlin.anomaly import OutlierDetector
   from pyod.models.pca import PCA

   # Read in vectors
   vectors = np.load('vectors.npy')

   # Initialize OD and thresholding model
   od = PCA(contamination=0.02)

   ml.set_experiment('outlier_model')
   clf = OutlierDetector(mlflow=True, detector=od)
   clf.fit(vectors)
   ml.end_run()

This anomaly model can be either logged using mlflow or simply as a
joblib file.

**Note** that a simpler encoder e.g. 384 dimesions leads to a "fuzzy"
outlier detector that is generally less strict and increases the
probability that new text and the embedded collection of text will have
a closer similarity. Higher dimesion encoder models can be used for a
dense embedded space e.g. over 2000 vectors or for strict settings e.g.
Medicine, but note that embedding time increases as well. Also, small
text collections <100 or collections with a wide range of topics may
degrade the filtering capabilities

Now that we have an anomaly model we can filter new incoming text. Here
is an example for a RAG setting:

.. code:: python

   from muzlin.anomaly import OutlierDetector
   from muzlin.encoders import HuggingFaceEncoder

   # Preload trained model - or load with joblib
   clf = OutlierDetector(model='outlier_detector.pkl')

   # Encode question
   encoder = HuggingFaceEncoder()

   vector = encoder(['Who was the first man to walk on the moon?'])
   vector = np.array(vector).reshape(1,-1) # Must be 2D

   # Get a binary inlier 0 or outlier 1 output
   label = clf.predict(vector)

The example above is just a quick dive into the capabilities of Muzlin.
Go check out the example notebooks for a more in depth tutorial on all
the different kinds of methods and possible applications.

***************
 Intergrations
***************

Muzlin supports the use of many libraries for both vector and graph
based setups, and is fully intergrated with MLFlow for model tracking
and Pydantic for validation.

+-----------------------------------+-------------------------+----------------------+
| Anomaly detection                 | Encoders                | Vector Index         |
+===================================+=========================+======================+
| -  Scikit-Learn                   | -  HuggingFace          | -  LangChain         |
| -  PyOD (vector)                  | -  OpenAI               | -  LlamaIndex        |
| -  PyGOD (graph)                  | -  Cohere               |                      |
| -  PyThresh (thresholding)        | -  Azure                |                      |
|                                   | -  Google               |                      |
|                                   | -  Amazon Bedrock       |                      |
|                                   | -  Fastembed            |                      |
+-----------------------------------+-------------------------+----------------------+

----

***********
 Resources
***********

**Table of notebooks**

+---------------------------+------------------------------------------------------------------------------------------------------+
| Notebook                  | Description                                                                                          |
+===========================+======================================================================================================+
| Introduction              | Data prep and a simple semantic vector-based outlier detection model                                 |
+---------------------------+------------------------------------------------------------------------------------------------------+
| Optimal Threshold         | Methods for optimal threshold selection (unsupervised, semi-supervised, supervised)                  |
+---------------------------+------------------------------------------------------------------------------------------------------+
| Cluster-Based Filtering   | Using clustering to decide if retrieved documents can answer a user's question                       |
+---------------------------+------------------------------------------------------------------------------------------------------+
| Graph-Based Filtering     | Using graph based anomaly detection for filtering semantic graph-based systems (e.g. GraphRAG)       |
+---------------------------+------------------------------------------------------------------------------------------------------+

************
 What Else?
************

Besides Muzlin there are also many other great libraries that can help
to increase a generative AI process flow. Check out `Semantic Router
<https://github.com/aurelio-labs/semantic-router>`_, `CRAG
<https://github.com/HuskyInSalt/CRAG>`_, and `Scikit-LLM
<https://github.com/iryna-kondr/scikit-llm>`_

----

**************
 Contributing
**************

**Note** at the moment their are major changes being done and the
structure of Muzlin is still being refined. For now, please leave a bug
report and potential new code for any fixes or improvements. You will be
added as a co-author if it is implemented.

Once this phase has been completed then ->

Anyone is welcome to contribute to Muzlin:

-  Please share your ideas and ask questions by opening an issue.

-  To contribute, first check the Issue list for the "help wanted" tag
   and comment on the one that you are interested in. The issue will
   then be assigned to you.

-  If the bug, feature, or documentation change is novel (not in the
   Issue list), you can either log a new issue or create a pull request
   for the new changes.

-  To start, fork the **dev branch** and add your
   improvement/modification/fix.

-  To make sure the code has the same style and standard, please refer
   to detector.py for example.

-  Create a pull request to the **dev branch** and follow the pull
   request template `PR template
   <https://github.com/KulikDM/muzlin/blob/main/.github/PULL_REQUEST_TEMPLATE.md>`_

-  Please make sure that all code changes are accompanied with proper
   new/updated test functions. Automatic tests will be triggered. Before
   the pull request can be merged, make sure that all the tests pass.
