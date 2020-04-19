from django.views.generic import View
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

class VoteView(View):
    """Base class to create a vote for a given model (question/answer)
    """
    model = None
    vote_model = None

    def get_vote_kwargs(self, user, vote_target):
        """
        This takes the user and the vote and adjusts the kwargs
        depending on the used model.
        """
        object_kwargs = {'user': user}
        object_kwargs['answer'] = vote_target

        return object_kwargs

    def post(self, request, pk):
        vote_target = get_object_or_404(self.model, pk=pk)

        #if vote_target.solver == request.user :
        #   raise ValidationError('Sorry, voting for your own answer is not possible.')

        #else:
        if True:
            upvote = request.POST.get('upvote', None) is not None
            object_kwargs = self.get_vote_kwargs(request.user, vote_target)
            vote, created = self.vote_model.objects.get_or_create(defaults={'value': upvote}, **object_kwargs)
            if created:

                if upvote:
                    vote_target.total_votes += 1

            else:
                if vote.value == upvote:
                    vote.delete()

                    if upvote:
                        vote_target.total_votes -= 1


                else:
                    vote.value = upvote
                    vote.save()
                    if upvote:
                        vote_target.total_votes  += 1
                    else:
                        vote_target.total_votes  -= 1


            vote_target.save()

        next_url = request.POST.get('next', '')
        if next_url != '':
            return redirect(next_url)

        else:
            return redirect(reverse_lazy('qa:all'))