(function ($) {
    "use strict"; // Start of use strict


    $(document).on('submit', '#newProject', function (event) {
        event.preventDefault()
        var serializedData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: 'create_project/',
            data: serializedData,
            success: postSuccess,
            error: postFail
        })
    })

    function postSuccess(data, textStatus, jqXHR) {
        $("#projects").load(" #projects");
        $('#newProject').trigger('reset')
        $("#project-creation").modal('hide')
    }

    function postFail(jqXHR, textStatus, errorThrown) {
        var responseText = jQuery.parseJSON(jqXHR.responseText);
        console.log(responseText)
        var error = Object.keys(responseText)[0];
        $("#message").html("<div class=\"alert alert-danger\" role=\"alert\">" + responseText[error] + "</div>")

    }

    let counter = 0;
    let milestone_id, feature_id;
    $('#update-milestone').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var milestone = button.data('whatever') // Extract info from data-* attributes
        var modal = $(this)
        modal.find('.modal-title').html('<strong>Update ' + milestone + '</strong>')
        modal.find('.modal-body').html('<div role="alert" class="alert alert-info"><span>' +
            '<strong>Note: </strong>Milestone names and features are cannot be changed.</span>')
        modal.find('.modal-body').append("<form id='features-form'>")
        // list the items
        milestone_id = button.attr('data')
        // parentId = button.closest('section').attr('id');
        var listItems = $("#features_" + milestone_id + ' li');
        listItems.each(function (idx, li) {
            var item = $(li).text()
            feature_id = $(li).attr('id')
            modal.find('.modal-body #features-form').append('<div class="form-row">' +
                '<div class="col xl-12">' +
                '<div class="form-group"><textarea type="text" class="form-control form-control-lg features" ' +
                'disabled readonly rows="2"> ' + item + '</textarea></div>' +
                '</div>' +
                '<div class="col-xl-4 ">' +
                '<div class="btn-group" role="group">' +
                '<button class="btn btn-primary btn-lg completed" id="' + $(li).attr('id') + '" type="button">' +
                'Mark as Completed</button>' +
                '<button class="btn btn-danger btn-lg delete" id="' + $(li).attr('id') + '" type="button">Remove</button></div>' +
                '</div></div><hr>')
        })
        modal.find('.modal-body').append('<button class="btn btn-primary btn-lg" id="add-feature"' +
            ' type="button">Add Feature</button>')
    })
    $(document).on('click', '#add-feature', function () {
        $('#update-milestone').find('.modal-body #features-form').append(
            '<div class="form-group">' +
            '<textarea type="text" id="featuremi' + counter + '" class="form-control form-control-lg" ' +
            'placeholder="Enter feature here." required></textarea>'
            + '</div>' +
            '<hr>')
        counter++;
    })

    $(document).on('click', '.completed', function () {

        $.ajax({
            type: 'POST',
            url: '../feature_complete/' + $(this).attr('id'),
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function () {
                $("#milestones").load(" #milestones");

            }
        })
    })
    $(document).on('click', '.delete', function () {

        $.ajax({
            type: 'POST',
            url: '../delete_feature/' + $(this).attr('id'),
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function () {
                $("#milestones").load(" #milestones");

            }
        })
    })
    $('#save').click(function () {

        // let list_features = $("#" + parentId + "-items")
        let features = []
        $('*[id*=featuremi]:visible').each(function () {
            let value = $(this).val();
            if (value.trim() != '') {
                features.push(value)
            }
        });
        $.ajax({
            type: 'POST',
            url: '../add_feature/' + milestone_id,
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                'features[]': features,
            },
            success: function () {
                $("#milestones").load(" #milestones");
            }
        })
        $("#update-milestone").modal('hide')

    })

    $(document).on('submit', '#updateDate', function (event) {
        event.preventDefault()
        $.ajax({
            type: "POST",
            url: '../update_date/' + $('#buttonDate').attr('data'),
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                date: $("#date").val()
            },
            success: function () {
                $('#project-header').load(' #project-header')
            }
        })
        console.log()
    })
    $(document).on('click', '#new-feature', function () {
        $('#new-milestone').find('.modal-body #features').append(
            '<div class="form-group">' +
            '<textarea type="text" id="featuremi_create' + counter + '"class="form-control form-control-lg"' +
            ' placeholder="Enter feature here." required></textarea>'
            + '</div>' +
            '<hr>')
        counter++;
    })
    $("#save-milestone").click(function (e) {
        // e.preventDefault();
        var milestone = new RegExp('^(Milestone|.+milestone)\\s[0-9]$', "g");
        //
        let milestone_name = $('input[name=name]').val().trim()
        let section_name = milestone_name.replace(' ', '-').toLowerCase()
        let list_name = section_name + '-items'
        if (milestone_name == '') {
            $("#new-milestone #name-validation").show().empty()
            $("#new-milestone #name-validation").append('<strong>Error:</strong> This field is required.')
            $('input[name=name]').css({border: '1px solid #e25865'})
        }
        // console.log(milestone.test(milestone_name));
        else if (!milestone.test(milestone_name)) {
            $("#new-milestone #name-validation").show().empty()
            $("#new-milestone #name-validation").append('<strong>Error:</strong> Invalid pattern. Please try again.')
            $('input[name=name]').css({border: '1px solid #e25865'})
        } else {
            let features = []
            $('#milestones').append('<section id="' + section_name + '">')
            $('#' + section_name).append('<h2><strong>' + milestone_name + '</strong></h2>' +
                '<p>' + milestone_name + ' means the following <span style="text-decoration: underline">are guaranteed</span> to be implemented.</p>' +
                '<ul id="' + list_name + '" class="big-list">')
            $('*[id*=featuremi_create]:visible').each(function () {
                let value = $(this).val();
                if (value.trim() != '') {
                    features.push(value)
                }
            });

            $.ajax({
                type: 'POST',
                url: '../new_milestone/',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    name: milestone_name,
                    'features[]': features,
                    project: $(this).attr('data')
                },
                success: function () {
                    $("#milestones").load(" #milestones");
                }
            })

            // $('#' + section_name).append('<button class="btn btn-info btn-lg" type="button" data-toggle="modal" ' +
            //     'data-target="#update-milestone" data-whatever="' + milestone_name + '">Update Milestone</button>')
            $("#new-milestone").modal('hide')
        }

    })


})(jQuery); // End of use strict
