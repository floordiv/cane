from core.objects.types import (FUNCTION)


indents = {
    FUNCTION: lambda source: '\n\n' + source + '\n'
}
