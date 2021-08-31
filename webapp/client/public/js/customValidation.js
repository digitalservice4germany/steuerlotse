/**
  * This is adapted from:
  *
  * @author ComFreek <https://stackoverflow.com/users/603003/comfreek>
  * @link https://stackoverflow.com/a/16069817/603003
  * @license MIT 2013-2015 ComFreek
  * @license[dual licensed] CC BY-SA 3.0 2013-2015 ComFreek
  * You MUST retain this license header!
*/
function inputMissingErrorMessageHelper(input_field, error_msg) {
    function inputMissing(){
        if (input_field.validity.valueMissing){
            input_field.setCustomValidity(error_msg);
        }
        else{
            input_field.setCustomValidity("");
        }
    }
    input_field.addEventListener("invalid", inputMissing);
}
