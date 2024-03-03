var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

dagfuncs.dynamicOptions = function (params, categories) {
    const selectedCategory = params.data.category;
    return {
        values: categories[selectedCategory],
    };
};