# VGSCode

Validate Generate Sanitize Code

List of supported codes:

1. Kazakhstan: IIN, BIN
2. ...

## Install

```sh
pip install vgscode
```

## Usage

```python
import vgscode
```

## Example

### validate

```python
vgscode.vBIN("320243026191"); #return True
vgscode.vIIN("320229474023"); #return False
```

### generate

```python
vgscode.gBIN("320243"); #return 320243952485
vgscode.gIIN("320229"); #return 320229980830
```

### sanitize

```python
vgscode.sNumberToString(320229474021); #return 320229474021
vgscode.sTrimStart("  320229474021"); #return 320229474021
vgscode.sTrimEnd("320229474021   "); #return 320229474021
vgscode.sTrimBoth("  320229474021  "); #return 320229474021
vgscode.sTrimAll("32 0229  4740 21"); #return 320229474021
vgscode.sRemoveNonDigits("320#%2294 74fwef021"); #return 320229474021
```
