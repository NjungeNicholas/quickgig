const CategoryPreview = () => {
    const Categories = [
        "Beauty & Grooming",
        "Errand Services",
        "Events & Catering",
        "Handywork",
        "Home Cleaning",
        "Pet Services",
        "Tech Support",
        "Tutoring & Education"
    ]
    return (
        <div className="mt-10">
            <h2 className="font-header text-text font-bold text-4xl text-center">Popular Categories</h2>
            <div className="flex flex-wrap gap-3 p-4 justify-center">
                {/* Category cards will go here */}
                {Categories.map((category, idx) =>
                    (<button key={idx} className="font-body font-bold text-secondary hover:text-primary py-4 px-4 rounded-full border-2 text-sm">
                        {category}
                    </button>
                    )
                )}
            </div>
        </div>
    );
}

export default CategoryPreview;
