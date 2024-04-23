var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

dagfuncs.dynamicOptions = function (params, categories) {
    // provides the conditional dropdown for subcategories
    const selectedCategory = params.data.category;
    return {
        values: categories[selectedCategory],
    };
};