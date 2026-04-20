def sqroots(coeffs:str) -> str:
    a, b, c = map(int, coeffs.split())
    D = b * b - 4 * a * c
    if D / (a ** 2) < 0:
        return ''
    elif D == 0:
        return str(-b / (2 * a))
    else:
        return f'{(-b + D ** 0.5) / (2 * a)} {(-b - D ** 0.5) / (2 * a)}'
