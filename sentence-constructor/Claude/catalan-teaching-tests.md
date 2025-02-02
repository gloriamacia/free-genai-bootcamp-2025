<test-cases>
    <case id="simple-1">
        <english>I eat bread.</english>
        <vocabulary>
            <word>
                <catalan>menjar</catalan>
                <english>eat</english>
                <notes>Regular -ar verb</notes>
            </word>
            <word>
                <catalan>pa</catalan>
                <english>bread</english>
                <notes>masculine noun</notes>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb] [Object].</structure>
        <considerations>
            - Basic sentence with subject, verb, and object
            - Present tense form
            - Subject pronouns can often be omitted in Catalan
        </considerations>
    </case>
    <case id="simple-2">
        <english>The book is red.</english>
        <vocabulary>
            <word>
                <catalan>llibre</catalan>
                <english>book</english>
                <notes>masculine noun</notes>
            </word>
            <word>
                <catalan>vermell</catalan>
                <english>red</english>
                <notes>adjective with gender agreement</notes>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb ser/estar] [Adjective].</structure>
        <considerations>
            - Simple descriptor sentence
            - Adjective agreement in gender and number
            - Uses ser for inherent qualities
        </considerations>
    </case>
</test-cases>

### 1.2 Compound Sentences
```xml
<test-cases>
    <case id="compound-1">
        <english>I eat bread and drink water.</english>
        <vocabulary>
            <word>
                <catalan>menjar</catalan>
                <english>eat</english>
            </word>
            <word>
                <catalan>pa</catalan>
                <english>bread</english>
            </word>
            <word>
                <catalan>beure</catalan>
                <english>drink</english>
            </word>
            <word>
                <catalan>aigua</catalan>
                <english>water</english>
                <notes>feminine noun</notes>
            </word>
        </vocabulary>
        <structure>[Subject] [Verb1] [Object1] i [Verb2] [Object2].</structure>
        <considerations>
            - Compound sentence with two actions
            - Subject shared between clauses
            - Uses "i" for conjunction
        </considerations>
    </case>
</test-cases>

### 1.3 Complex Sentences
```xml
<test-cases>
    <case id="complex-1">
        <english>Because it's hot, I drink water.</english>
        <vocabulary>
            <word>
                <catalan>fer calor</catalan>
                <english>to be hot (weather)</english>
                <notes>impersonal expression</notes>
            </word>
            <word>
                <catalan>beure</catalan>
                <english>drink</english>
            </word>
            <word>
                <catalan>aigua</catalan>
                <english>water</english>
            </word>
        </vocabulary>
        <structure>[Conjunction] [Weather Expression], [Subject] [Verb] [Object].</structure>
        <considerations>
            - Cause and effect relationship
            - Uses "perquè" for "because"
            - Weather expressions using "fer"
        </considerations>
    </case>
</test-cases>

## 2. Vocabulary Edge Cases

### 2.1 Multiple Meanings
```xml
<vocabulary-test>
    <word>
        <catalan>quedar</catalan>
        <meanings>
            <meaning>to stay</meaning>
            <meaning>to meet up</meaning>
            <meaning>to remain</meaning>
        </meanings>
        <test-sentences>
            <sentence>Em quedo a casa.</sentence>
            <sentence>Quedem a les sis?</sentence>
            <sentence>Queda poc pa.</sentence>
        </test-sentences>
    </word>
</vocabulary-test>

### 2.2 Ser/Estar Usage
```xml
<vocabulary-test>
    <pair>
        <ser>
            <catalan>ser</catalan>
            <english>to be (permanent/inherent)</english>
            <test-sentences>
                <sentence>Sóc català.</sentence>
                <sentence>És un llibre.</sentence>
            </test-sentences>
        </ser>
        <estar>
            <catalan>estar</catalan>
            <english>to be (temporary/condition)</english>
            <test-sentences>
                <sentence>Estic cansat.</sentence>
                <sentence>Està a Barcelona.</sentence>
            </test-sentences>
        </estar>
    </pair>
</vocabulary-test>

## 3. State Transition Tests

### 3.1 Valid Transitions
```xml
<transition-test>
    <scenario id="setup-to-attempt">
        <initial-state>Setup</initial-state>
        <input>Menjo pa.</input>
        <expected-state>Attempt</expected-state>
        <validation>
            - Input contains Catalan text
            - No question marks
            - Contains vocabulary from setup
        </validation>
    </scenario>
    <scenario id="attempt-to-clues">
        <initial-state>Attempt</initial-state>
        <input>How do I use definite articles?</input>
        <expected-state>Clues</expected-state>
        <validation>
            - Input is a question
            - References grammar concept
            - Related to previous attempt
        </validation>
    </scenario>
</transition-test>

## 4. Teaching Scenario Tests

### 4.1 Common Mistakes
```xml
<teaching-test>
    <scenario id="article-mistake">
        <student-attempt>El aigua és freda.</student-attempt>
        <error>Incorrect article with feminine noun starting with stressed 'a'</error>
        <expected-guidance>
            - Acknowledge attempt
            - Explain article rules for feminine nouns
            - Encourage new attempt
        </expected-guidance>
    </scenario>
    <scenario id="verb-conjugation">
        <student-attempt>Jo soc estudiant.</student-attempt>
        <error>Incorrect spelling of "sóc"</error>
        <expected-guidance>
            - Point out accent rules
            - Review present tense of ser
            - Encourage correction
        </expected-guidance>
    </scenario>
</teaching-test>

## 5. Validation Criteria

### 5.1 Response Scoring
```xml
<scoring-criteria>
    <category name="vocabulary-table">
        <criteria>
            - Contains all necessary words (2 points)
            - Correct gender/number marking (2 points)
            - Infinitive forms for verbs (2 points)
            - Articles properly listed (2 points)
            - Appropriate difficulty level (2 points)
        </criteria>
    </category>
    <category name="sentence-structure">
        <criteria>
            - Clear word order (2 points)
            - Proper verb conjugation (2 points)
            - Article-noun agreement (2 points)
            - Adjective placement/agreement (2 points)
            - Appropriate pronouns (2 points)
        </criteria>
    </category>
</scoring-criteria>

## 6. Documentation Improvements

### 6.1 Version Control
```xml
<version-control>
    <version number="1.0">
        <changes>
            - Initial test documentation
            - Basic test cases added
            - State transition examples
        </changes>
        <date>2025-01-03</date>
    </version>
    <planned-improvements>
        - Add more verb tense examples
        - Expand pronoun usage cases
        - Include dialectal variations
        - Add cultural context tests
    </planned-improvements>
</version-control>

### 6.2 Cross-References
```xml
<cross-references>
    <reference id="articles">
        <related-sections>
            - Vocabulary Table Guidelines
            - Common Mistakes
            - Teaching Scenarios
        </related-sections>
        <purpose>Ensure consistent article handling across documentation</purpose>
    </reference>
    <reference id="verb-conjugation">
        <related-sections>
            - Sentence Structure Guidelines
            - Teaching Scenarios
            - Validation Criteria
        </related-sections>
        <purpose>Maintain consistent conjugation patterns</purpose>
    </reference>
</cross-references>