from otter_welcome_buddy.startup import cogs


def test_formatModulePath_cogExtensionFormat():
    # Arrange
    cog_path = cogs.new_user_joins.__file__

    # Act
    format_path = cogs.__format_module_path_into_cog_extension(cog_path)

    # Assert
    assert format_path == "cogs.new_user_joins"
