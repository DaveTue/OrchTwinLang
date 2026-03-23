import FreeCAD
import Part

# Function to create a simple box
def create_box(length, width, height):
    doc = FreeCAD.newDocument("BoxDocument")
    box = doc.addObject("Part::Box", "MyBox")
    box.Length = length
    box.Width = width
    box.Height = height
    doc.recompute()
    return box

# Function to get dimensions of the box
def get_box_dimensions(box):
    return box.Length, box.Width, box.Height

# Function to update the dimensions of the box
def set_box_dimensions(box, length, width, height):
    box.Length = length
    box.Width = width
    box.Height = height
    FreeCAD.ActiveDocument.recompute()

# Main execution
if __name__ == "__main__":
    length, width, height = 10, 10, 10
    box = create_box(length, width, height)

    # Get dimensions
    print("Initial Dimensions:", get_box_dimensions(box))

    # Update dimensions
    set_box_dimensions(box, 20, 15, 10)
    print("Updated Dimensions:", get_box_dimensions(box))
