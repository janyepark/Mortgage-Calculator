""" Test the mortgage calculation homework. """
# replace mortgage below with the name of your script (without the .py).
import mortgage as mort
from collections import Counter
from copy import deepcopy
import inspect
from math import isclose
class ParameterError(Exception):
    pass
class ParamCheck:
    """ Analyze a function's parameters and make it possible to pass
    arguments based on the default values of the function's parameters.
    
    Attributes:
        func (function): the function whose parameters are being
            checked.
    """
    def __init__(self, func, expected_required, expected_defaults,
                 check_optional_order=False):
        self.func = func
        self.required, self.optional = self.analyze_params(func)
        defaults = [v[1] for v in self.optional]
        try:
            self.check_required(len(self.required), expected_required)
            self.check_optional(defaults, expected_defaults,
                                check_order=check_optional_order)
        except ParameterError as e:
            raise e
    
    def analyze_params(self, func):
        """ Extract information about the required and optional
        parameters of the function.
        
        Args:
            func (function): the function whose parameters are being
                analyzed.
        
        Returns:
            tuple of (list of str), (list of tuple of (str, value))
        """
        signature = inspect.signature(func)
        actual_req = []       # names of required arguments
        actual_opt = []       # default values of optional arguments
        for name, param in signature.parameters.items():
            if param.default is inspect.Parameter.empty:
                actual_req.append(name)
            else:
                actual_opt.append((name, param.default))
        return actual_req, actual_opt
    def check_required(self, num_actual, num_expected):
        """ Ensure that function has the correct number of required
        parameters.
        
        Args:
            num_actual (int): the number of required parameters the
                function actually has.
            num_expected (int): the number of required parameters the
                function should have.
        
        Returns:
            None: no error was encountered.
            
        Raises:
            ParameterError: function has an unexpected number of
                required parameters.
        """
        if num_actual != num_expected:
            msg = (f"function {func.__name__} has {num_actual}"
                   f" required parameters (it should have {num_expected})")
            raise ParameterError(msg)
    
    def check_optional(self, actual_defaults, expected_defaults,
                       check_order=False):
        """ Ensure that the function has the right number of optional
        parameters and that those optional parameters have the default
        values we expect, in the order in which we expect them.
        
        Args:
            actual_defaults (list of values): the actual default values
                of the function's optional parameters.
            expected_defaults (list of values): the expected default
                values for the function's optional parameters.
            check_order (bool): if True, ensure the default values occur
                in the expected order.
        
        Returns:
            None: no error was encountered.
        
        Raises:
            ParameterError: the function does not satisfy the stated
                expectations regarding default values of optional
                parameters.
        """
        if sorted(actual_defaults) != sorted(expected_defaults):
            expected_count = Counter(expected_defaults)
            actual_count = Counter(actual_defaults)
            missing = expected_count - actual_count
            extra = actual_count - expected_count
            msg = f"in function {self.func.__name__}, "
            if missing:
                msg += ("missing parameters with the following default values:"
                       + ", ".join(str(v) for v in missing))
            if extra:
                if missing:
                    msg += "; "
                msg += ("encountered parameters with the following unexpected"
                        " default values:"
                        + ", ".join(str(v) for v in extra))
            raise ParameterError(msg)
        if check_order and actual_defaults != expected_defaults:
            raise ParameterError()
    
    def invoke(self, args, opt_args):
        """ Invoke the function using default values instead of keyword
        arguments for the optional parameters.
        
        Args:
            args (list of values): the arguments to pass to the required
                parameters of the function.
            opt_args (list of (tuple of value, value)): the values to
                pass to the optional parameters of the function. Each
                item in the list is a tuple where the first value is the
                default value associated with an optional parameter, and
                the second value is the value to use for that parameter.
                
                If multiple optional parameters have the same default
                value, arguments for those parameters will be assigned
                in order (so, for example, if the function has
                parameters x=0 and y=0, declared in that order, and
                opt_args is [(0, 4), (0, 5)], x will get the value 4 and
                y will get the value 5).
        
        Returns:
            The result of the function invocation.
            
        Raises:
            RuntimeError: an error was encountered while running the
                function.
        """
        if len(args) != len(self.required):
            raise ValueError("wrong number of required arguments specified")
        kwargs = {}
        options = deepcopy(self.optional)
        for dflt, value in opt_args:
            for n, (name, dflt2) in enumerate(options):
                if dflt == dflt2:
                    kwargs[name] = value
                    options.pop(n)
                    break
            else:
                raise ValueError(f"can't find option with default value {dflt}")
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            argstr = ", ".join(str(a) for a in args)
            kwargstr = ", ".join(f"{kw}={val}" for (kw, val) in kwargs.items())
            arg_msg = (f"{argstr}, {kwargstr}" if argstr and kwargstr
                       else argstr if argstr
                       else kwargstr if kwargstr
                       else "")
            msg = (f"while running {self.func.__name__}({arg_msg}), an error"
                   " occurred")
            raise RuntimeError(msg) from e
                 
def test_get_min_payment():
    """ Test get_min_payment() """
    defaults = [30,12]
    try:
        pc = ParamCheck(mort.get_min_payment, expected_required=2,
                        expected_defaults=defaults)
    except ParameterError as e:
        raise e
    assert mort.get_min_payment(0, 1) == 0
    result = mort.get_min_payment(100_000, 0.03)
    assert result == 422
    assert isinstance(result, int)
    assert pc.invoke(args=[300_000, 0.05], opt_args=[(30, 15)]) == 2373
    assert pc.invoke(args=[300_000, 0.05], opt_args=[(30, 15), (12, 6)]) == 4752
def test_interest_due():
    """ Test interest_due() """
    defaults = [12]
    try:
        pc = ParamCheck(mort.interest_due, expected_required=2,
                        expected_defaults=defaults)
    except ParameterError as e:
        raise e
    assert isclose(mort.interest_due(400_000, 0.03), 1000)
    assert isclose(pc.invoke(args=[400_000, 0.03], opt_args=[(12, 6)]),
                   2000)
def test_remaining_payments():
    """ Test remaining_payments() """
    defaults = [12]
    try:
        pc = ParamCheck(mort.remaining_payments, expected_required=3,
                        expected_defaults=defaults)
    except ParameterError as e:
        raise e
    assert mort.remaining_payments(200_000, 0.04, 955) == 360
    assert pc.invoke(args=[200_000, 0.04, 5000], opt_args=[(12, 4)]) == 52
