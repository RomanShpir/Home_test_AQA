from test_scripts.main_ui import Ui


def test_ui_navigate_base_page(ui: Ui):
    """
    Test to navigate to the base page and verify the title.
    """
    game_category = "StarCraft II"
    ui.navigation.open_base_page()
    ui.navigation.menu_click("Browse")
    ui.navigation.locate_and_close_app_use_popup()
    ui.browse_page.input_search_category_name(category_name=game_category)
    ui.browse_page.verify_category_present(category_name=game_category)
    ui.browse_page.select_category_from_search_results(category_name=game_category)
    ui.navigation.scroll_bottom_of_page(times_to_scroll=2)
    ui.browse_page.open_random_available_stream()
    ui.browse_page.wait_for_stream_to_load()
    ui.navigation.clear_popup_windows()
