from data_module import (
    display_dataset_preview,
    display_visualisation,
    search_data,
    update_data_entry,
    save_changes
)

def main_menu():
    while True:
        print("\n=== Data Viewer Interface ===")
        print("1. View dataset")
        print("2. View visualisation")
        print("3. Search or filter data")
        print("4. Update a data entry")
        print("5. Save changes")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            display_dataset_preview()
        elif choice == '2':
            display_visualisation()
        elif choice == '3':
            search_data()
        elif choice == '4':
            update_data_entry()
        elif choice == '5':
            save_changes()
            print("Changes saved.")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main_menu()