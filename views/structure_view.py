import streamlit as st


def generate_structure_view():
    st.title(':green[Sheet structure]')

    create = '''How to define, instantiate or create the data type, possibly from other types.  
    <span class="example">Examples: define a date, parse date from string, create set from a list of values</span>
    '''

    test = '''Check or assess something about the object.  
    <span class="example">Examples: is it empty? does it contain a given value?</span>
    '''

    extract = '''Get properties, attributes, or other information about the object _of a different type than the object_ (typically scalars).  
    <span class="example">Examples: length of a list, element value at a given index, max value among elements.</span>
    '''

    derive = '''Create a derived or altered object from the given object, preserving the object type, or _update_ the object in-place / by-reference.  
    <span class="example">Examples: head of a list, slicing a string, selecting conditional rows from a data frame.</span>
    '''

    convert = '''Export / represent the object as a different data type.  
    <span class="example">Examples: datetime as string, dictionary as list of key-value pairs, data frame as matrix.</span>
    '''

    st.markdown(
        f'''
    This page describes the common structure of _actionsheets_.
    
    Most actionsheets describe how to create and manipulate a specific data type or object.
    For example, there are actionsheets about strings, lists, and data.frames. 
    
    Sheets are hierarchically structured using sections. The main sections are:
        
    1. **[:orange[Create]](#create)**  
    {create}
    2. **[:orange[Test]](#test)**  
    {test}
    3. **[:orange[Extract]](#extract)**  
    {extract}
    4. **[:orange[Derive / Update]](#derive-update)**  
    {derive}
    5. **[:orange[Convert]](#convert)**  
    {convert}
    
    Additional common categories, used when applicable:
    - **:orange[Constants]**: 
    Available constants, defaults, or singleton
    - **:orange[Usage]**: 
    Specific syntax, statements, or recommended patterns.
    - **:orange[Iterate]**: 
    Operations that iterate or traverse through the object (its elements, keys, rows, nodes).
    - **:orange[Install]**:
    Installation instructions.
    - **:orange[Show]**:
    Ways to print or visualize the object in a human-readable way.
        ''', unsafe_allow_html=True
    )

    st.markdown(
        f'''
    ---
    # Create
    {create}
        
    # Test
    {test}
        
    # Extract
    {extract}
        
    ##### Subcategories
    - **:orange[Properties]**  
    Operations which retrieve properties or attributes of the object.  
    <span class="example">Examples: length of a list, number of columns of a data frame.</span>
    - **:orange[Find]**  
    Operations which attempt to find a value or index of an object, typically with index output.  
    <span class="example">Examples: find max value, find index of min value, find key of most frequent value</span>
    - **:orange[Aggregate]**  
    Operations which aggregate the object in a way that involves a computation, typically with scalar output.  
    <span class="example">Examples: sum all elements of a list, number of occurrences per value</span>
           
    # Derive / update
    {derive}
        
    ##### Subcategories
    - **:orange[Transform]**  
    Operations that apply a [transformation](https://en.wikipedia.org/wiki/Data_transformation_(statistics)) to the object or each of its elements, preserving the shape of the object.  
    <span class="example">Examples: element-wise operations such as adding a constant to a vector, or computing the cumulative sum over the elements</span>
      - **:orange[Mask]**  
      Generate a boolean mapping. Typically used as a _logical mask_ or _logical index_ for filtering elements in later operations.  
    - **:orange[Order]**  
    Operations which change the order of elements, but not their values.  
    <span class="example">Examples: reversing the elements of a list, sorting a data frame by column values</span>
    - **:orange[Reshape]**  
    Operations which change the shape of the object, but preserves all elements.  
    <span class="example">Examples: transposing a matrix, converting a data frame to narrow format.</span>
    - **:orange[Grow]**  
    Operations which possibly increase the number of elements of the object.  
    <span class="example">Examples: appending elements to a list, replicating elements.</span>
        - **:orange[Add]**  
        Add one or more new elements. 
        - **:orange[Replicate]**  
        Operations which increase the number of elements through replication or derivation.
    - **:orange[Shrink]**  
    Operations which possibly reduce the number of elements of the object.  
    <span class="example">Examples:  Removing elements from a list, removing duplicates.</span>
        - **:orange[Remove]**  
        Remove one or more elements. 
        - **:orange[Aggregate]**  
        Operations which aggregate elements by some grouping logic.
    - **:orange[Combine]**  
    Operations which combines, merge or joins two or more objects.
    The number of elements may grow or shrink, depending on the operation and input.  
    <span class="example">Examples: stacking lists, set union, joining two data frames.</span>

    # Convert
    {convert}
    Elements are preserved unless mentioned otherwise. However, some attributes may be lost in the process.
    ''', unsafe_allow_html=True
    )

    st.html('''
    <style>
        h1 { color: var(--section-color); }
        .example { color: #FFE1A5; font-style: italic; }
    </style>
    ''')
