-- stored procedure to compute the average score for a user

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    UPDATE users
    SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = p_user_id)
    WHERE id = p_user_id;
END //
DELIMITER ;
