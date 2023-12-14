$(document).ready(function() {
    $(".show-details-btn").on("click", function() {
        var productUuid = $(this).data("product-uuid");
        var productSlug = $(this).data("product-slug");

        // AJAX request to fetch product details
        $.ajax({
            url: `/${productUuid}/${productSlug}/`,
            type: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            success: function(data) {

                console.log(data.product_url);

                $("#product-name").text(data.name);
                $("#product-category").text(data.category);
                $("#product-description").html(data.description);
                $("#product-image").attr("src", data.image);
                $("#see-product-url").attr("href", data.product_url);
                if (data.discounted_price != data.price) {
                    $("#product-price").text("$" + data.discounted_price);
                    $("#product-original-price").text("$" + data.price);
                    $("#discount_percent").text("%" + (100-(data.discounted_price/data.price)*100));
                    $("#product-original-price").css("visibility", "visible");
                    $("#discount_percent").css("visibility", "visible");
                } else {
                    $("#product-price").text("$" + data.price);
                    $("#product-original-price").css("visibility", "hidden");
                    $("#discount_percent").css("visibility", "hidden");
                }
                


                // Update the Facebook share link element
                $("#facebook-share-btn").attr("href", facebookShareLink);




                // Show the modal
                $("#product-details-modal").show();
            },
            error: function(error) {
                console.log("Error fetching product details:", error);
            }
        });
    });

    // Close the modal when the close button is clicked
    $(".close").on("click", function() {
        $("#product-details-modal").hide();
    });
});








