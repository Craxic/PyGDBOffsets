# Thanks to FatalError from https://stackoverflow.com/questions/9788679/ for providing the base for this

import gdb
import pprint
import sys
import os

def create_table(rows, rowTypes):
    """
    rows is a list of lists of strings
    rowTypes indicates alignment. 1 character per column.
    """
    if len(rows) == 0:
        return "";
        
    returnString = "";
    
    # Make everything a string
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = str(rows[i][j])
    
    # Calculate max width of columns
    column_widths = [0] * len(rows[0]);
    for row in rows:
        for i, item in enumerate(row):
            column_widths[i] = max(column_widths[i], len(item));
    
    # Create formatter
    row_format = "";
    for i, col in enumerate(column_widths):
        row_format += "{:" + rowTypes[i] + str(col) + "}";
    
    # Print using formatter
    for row in rows:
        returnString += row_format.format(*row) + "\n"
    
    return returnString;
        
def get_fields(rows, stype, offset, indent, verbose_mode, current_pos_string):
    """
    Adds a row to the list "rows" for every field in "stype".
    
    Offset is a number. If negative, offset indicates that this type is not a part of the 
    serialization of the parent type.
    
    Indent is prepended to the entry in the first column for clarity.
    """
    for field in stype.fields():
        # If the field has the "BitPos" attribute, then it is a part of the serialisation of the 
        # parent type. Things that don't have this include static fields and the possible values of 
        # an enum type.
        pos_decimal = '';
        
        if (hasattr(field, 'bitpos')):
            if field.name is None:
                pos = "<range type?>"; # occurs for range-type fields (Arrays expand into 1 of these)
            elif not field.is_base_class:
                eval_string = "&(" + current_pos_string + str(field.name) + ")";
                try:
                    pos = str(gdb.parse_and_eval(eval_string));
                except gdb.error:
                    pos = "<error evaluating \"" + eval_string + "\">";
                    
                if pos.startswith("0x"):
                    pos_decimal = " (" + str(int(pos, 0)) + ")"
            else:
                pos = "<base type>";
        else:
            pos = '?'; # Not in an instance.
        
        field_type = str(field.type);
        if field.type.code == gdb.TYPE_CODE_TYPEDEF:
            field_type += " (aka " + str(field.type.strip_typedefs()) + ")";
        
        # field.type is None when this is a possible value of an enum type
        size = 0 if field.type is None else field.type.sizeof;
        
        # Get the offset of the type in the parent struct (or ? if we're not in its serialization)
        if offset < 0 or pos == '?':
            offset_str = '?'
        else:
            offset_str = str(offset);
            
        # Do we need to go deeper?
        if field.type is not None:
            try:
                this_fields = field.type.fields()
                if (len(this_fields) == 0):
                    this_fields = None;
            except TypeError:
                this_fields = None; # field.type.fields() fails for integral types (unsigned int, etc.)
        else:
            this_fields = None
        
        # Append the row for output
        is_real = offset >= 0 and size > 0 and pos != '?';
        if verbose_mode or is_real:
            is_integral = this_fields is None and is_real;
            indent_mod = ('>' if is_integral else ' ') + indent # Add a ">" if this is an integral type.
            rows.append([
                indent_mod + str(field_type), 
                ' ', 
                field.name,
                " = char[", size , "] at ",
                str(pos), 
                pos_decimal,
                ' <' if is_integral else ''
                ]);
        
            # Do we need to go deeper?
            if this_fields is not None:
            
                new_pos_string = current_pos_string;
                if not field.is_base_class:
                    new_pos_string = current_pos_string + str(field.name) + ".";
                    
                get_fields(rows, field.type, -1 if pos == '?' else offset, indent + "    ", verbose_mode, new_pos_string);
        
        # Increase offset if this type is really in the parent type.
        if offset >= 0:
            offset += int(size) if pos != '?' else 0;

def show_usage():
    raise gdb.GdbError('Usage: \"offsets-of [-v] ClassOrStructType\". -v lists fields that don\'t effect size.')

class Offsets(gdb.Command):
    def __init__(self):
        super (Offsets, self).__init__ ('offsets-of', gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        
        if len(argv) == 0:
            show_usage();
        
        # Get the parameters
        verbose_mode = '-v' in argv;
        class_name = argv[len(argv) - 1];

        try:
            # Look up class
            stype = gdb.lookup_type(class_name)

            # Print name and size
            print(stype.name + '[' + str(stype.sizeof) + '] {');
            
            # Add the fields to a list and print them using create_table.
            rows = [];
            get_fields(rows, stype, 0, "    ", verbose_mode, "(("+stype.name+"*)0)->");
            print(create_table(rows, "<<<<><>>>") + "}")
            
        except BaseException as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e), exc_type, fname, exc_tb.tb_lineno);

Offsets()