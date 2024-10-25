# Pussy
## Idea
This libary is ment to be used as a help to find out if you can find the clit or not.
## Example usage
Here is an example on how to use the libary:

```python
from pussy import Pussy, ClitNotFoundException

def main():
    pussy = Pussy("men")
    try:
        print(pussy.find_clit())
    except ClitNotFoundException as e:
        print(e)

if __name__ == "__main__":
    main()
```
